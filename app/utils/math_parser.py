import re
import time
from typing import List, Dict, Any

class MathParser:
    """Handles parsing and evaluation of mathematical expressions from bill text"""
    
    def __init__(self):
        # Common mathematical operators and symbols
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else 0,
            'x': lambda x, y: x * y,
            'X': lambda x, y: x * y
        }
        # List of known product names with numbers to ignore
        self.known_numbered_products = [
            '7up', '5 star', '7 up', '7-up', '5star', '7up', '7-up', '7 Up', '5Star', '7UP', '5STAR', '7 UP', '5 STAR',
            # Add more as needed
        ]
        # Patterns for different bill formats
        self.patterns = [
            r'(\d+(?:\.\d+)?)\s*[xX]\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)',  # 2 x 10 = 20
            r'(\d+(?:\.\d+)?)\s*[*]\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)',   # 2 * 10 = 20
            r'(\d+(?:\.\d+)?)\s*[+]\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)',   # 10 + 20 = 30
            r'(\d+(?:\.\d+)?)\s*[-]\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)',   # 50 - 10 = 40
            # Only match numbers at the end of the line or after currency symbols
            r'(?:\$|Rs\.?|INR)?\s*(\d+(?:\.\d+)?)(?=\s*$)',  # e.g. ... 20.00
        ]
    
    def parse_and_calculate(self, text: str) -> Dict[str, Any]:
        """
        Parse text and extract mathematical calculations
        
        Args:
            text (str): Text extracted from bill image
            
        Returns:
            dict: Parsed results with lines and total
        """
        start_time = time.time()
        
        try:
            lines = text.strip().split('\n')
            parsed_lines = []
            total = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Parse the line
                parsed_line = self._parse_line(line)
                if parsed_line:
                    parsed_lines.append(parsed_line)
                    # Add calculated value to total
                    if 'calculated' in parsed_line:
                        total += parsed_line['calculated']
            
            processing_time = time.time() - start_time
            
            return {
                'lines': parsed_lines,
                'total': round(total, 2),
                'processing_time': round(processing_time, 3)
            }
            
        except Exception as e:
            raise Exception(f"Error parsing mathematical expressions: {str(e)}")
    
    def _parse_line(self, line: str) -> Dict[str, Any]:
        """
        Parse a single line for mathematical expressions
        
        Args:
            line (str): Single line of text
            
        Returns:
            dict: Parsed line information
        """
        try:
            # Clean the line
            cleaned_line = self._clean_line(line)
            # Lowercase for product name matching
            line_lower = line.lower()
            # Ignore lines that are just product names with numbers
            for prod in self.known_numbered_products:
                if prod in line_lower:
                    # If the line is just a product name or starts with a product name, skip extracting numbers
                    # But if there is a price at the end, still allow it
                    # e.g. "7UP 2 40.00" should allow 40.00 as price
                    # If the only numbers are part of the product name, skip
                    # If there is a number at the end, allow
                    # We'll handle this below
                    break
            # Try to match different patterns
            for pattern in self.patterns:
                match = re.search(pattern, cleaned_line)
                if match:
                    if len(match.groups()) == 3:  # Full expression with result
                        num1, num2, result = map(float, match.groups())
                        calculated = self._evaluate_expression(num1, num2, line)
                        return {
                            'text': line,
                            'numbers': [num1, num2],
                            'result': result,
                            'calculated': calculated,
                            'confidence': 0.9 if abs(calculated - result) < 0.01 else 0.7
                        }
                    elif len(match.groups()) == 1:  # Just a number (at end or after currency)
                        num = float(match.group(1))
                        # Only treat as price if at end of line or after currency
                        if self._is_price_candidate(line, num):
                            return {
                                'text': line,
                                'numbers': [num],
                                'calculated': num,
                                'confidence': 0.8
                            }
            # If no pattern matches, try to extract numbers at the end of the line
            numbers = self._extract_numbers(line)
            if numbers:
                # Only add the last number if it's at the end of the line and not part of a product name
                last_number = numbers[-1]
                if self._is_price_candidate(line, last_number):
                    return {
                        'text': line,
                        'numbers': [last_number],
                        'calculated': last_number,
                        'confidence': 0.6
                    }
            return None
        except Exception as e:
            return {
                'text': line,
                'error': str(e),
                'calculated': 0,
                'confidence': 0.0
            }
    
    def _clean_line(self, line: str) -> str:
        """
        Clean line for better parsing
        
        Args:
            line (str): Raw line text
            
        Returns:
            str: Cleaned line
        """
        # Remove extra spaces
        line = re.sub(r'\s+', ' ', line.strip())
        
        # Normalize multiplication symbols
        line = re.sub(r'[xX]', '*', line)
        
        # Remove common non-mathematical words
        words_to_remove = ['total', 'subtotal', 'sum', 'amount', 'price', 'cost']
        for word in words_to_remove:
            line = re.sub(rf'\b{word}\b', '', line, flags=re.IGNORECASE)
        
        return line.strip()
    
    def _extract_numbers(self, text: str) -> List[float]:
        """
        Extract all numbers from text, but ignore numbers that are part of known product names
        """
        # Remove known product names with numbers before extracting
        text_clean = text
        for prod in self.known_numbered_products:
            text_clean = re.sub(prod, '', text_clean, flags=re.IGNORECASE)
        numbers = re.findall(r'\d+(?:\.\d+)?', text_clean)
        return [float(num) for num in numbers]
    
    def _evaluate_expression(self, num1: float, num2: float, line: str) -> float:
        """
        Evaluate mathematical expression based on operators found in line
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            line (str): Original line text
            
        Returns:
            float: Calculated result
        """
        # Determine operator from line
        if '*' in line or 'x' in line.lower():
            return num1 * num2
        elif '+' in line:
            return num1 + num2
        elif '-' in line:
            return num1 - num2
        elif '/' in line:
            return num1 / num2 if num2 != 0 else 0
        else:
            # Default to multiplication for bill calculations
            return num1 * num2
    
    def safe_eval(self, expression: str) -> float:
        """
        Safely evaluate mathematical expression
        
        Args:
            expression (str): Mathematical expression string
            
        Returns:
            float: Result of evaluation
        """
        try:
            # Only allow safe characters
            safe_chars = set('0123456789+-*/.() ')
            if not all(c in safe_chars for c in expression):
                raise ValueError("Expression contains unsafe characters")
            
            # Evaluate the expression
            result = eval(expression)
            return float(result)
            
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{expression}': {str(e)}") 

    def _is_price_candidate(self, line: str, number: float) -> bool:
        """
        Heuristic: Only treat a number as a price if it is at the end of the line, after a currency symbol, or separated by space from product names.
        """
        # Check for currency symbol before the number
        currency_patterns = [r'\$\s*'+str(number), r'Rs\.?\s*'+str(number), r'INR\s*'+str(number)]
        for pat in currency_patterns:
            if re.search(pat, line):
                return True
        # Check if number is at the end of the line
        if re.search(r'(\d+(?:\.\d+)?)\s*$', line) and str(number) in line:
            # Make sure it's not part of a product name
            for prod in self.known_numbered_products:
                if prod in line.lower() and str(int(number)) in prod:
                    return False
            return True
        return False 