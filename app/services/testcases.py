
from app.helper.error_handling import MissingParameterException
from app.helper.gpt import get_chat_completion
from flask import jsonify , request
import os

def generate_test_cases(java_class_code, java_class_name):
    try:
        if not java_class_code:
            raise MissingParameterException('java_class_code')
        
        prompt = f'''
        Inputs Provided:
        Java Class:
        ```
        {java_class_code}
        ```
        
        
Generate JUnit test cases for the given Java class while following the below JaCoCo test coverage verification rules:

1. **General Rules**:
   - The test cases should achieve at least **80% line coverage**.
   - Avoid generating tests for excluded packages: **config, model, entity, exception, utils, constant, event, domain**.
   - Exclude classes with names ending in `Application`, `MapperImpl`, `FullProfileDataMapper*`, `RequestResponseLoggingFilter`.

2. **Coverage Limits**:
   - **Line Coverage**: Minimum **90%**
   - **Branch Coverage**: **100%**
   - **Class Level Line Coverage**: Minimum **90%**

3. **Test Case Considerations**:
   - Cover all possible logic branches, including **all conditional statements, loops, and switch cases**.
   - Include edge cases, boundary values, and negative test cases.
   - Ensure **exception scenarios are covered** using `assertThrows`.
   - Use appropriate assertions to validate method outputs.
   - Ensure the test cases follow best practices for unit testing.
   - Add assertions in all test cases to validate expected outputs.
   - **For each model or entity inside the class, create mock data using Mockito.**
   - **For every private method in the class, test them using Reflection:**
     - Retrieve the private method using `Class.getDeclaredMethod()`.
     - Set the method as accessible using `setAccessible(true)`.
     - Invoke the method using `Method.invoke()`, passing required parameters.
     - Validate the return values using assertions.
   - **Mock all external service calls, repositories, and dependencies using Mockito to prevent integration failures.**
   - **Ensure all constructors, getters, and setters in the class are tested if applicable.**
   
    Generate well-structured JUnit test cases in a proper Java file format using **JUnit 5 and Mockito**, implementing reflection-based testing for private methods where applicable.

        '''

        
        response = get_chat_completion(prompt)
        test_case_file_name = f"{java_class_name}Test.java"
        test_case_file_path = os.path.join("/tmp", test_case_file_name)
        
        with open(test_case_file_path, "w") as test_case_file:
            test_case_file.write(response.strip())
        
        return test_case_file_path
    
    except MissingParameterException as e:
        return jsonify({'error': e.message}), 400
    
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
