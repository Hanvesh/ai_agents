from app.helper.error_handling import MissingParameterException
from app.helper.gpt import get_chat_completion
from flask import jsonify
import os

def generate_crud_from_ddl(ddl_command, package_name):
    try:
        if not ddl_command:
            raise MissingParameterException('ddl_command')
        if not package_name:
            raise MissingParameterException('package_name')

        prompt = f"""
        You are an expert Spring Boot developer and software architect.
        Your task is to generate a complete, production-grade CRUD API layer based on the provided DDL command.

        Inputs Provided:
        Package Name: {package_name}
        DDL Command:
        ```
        {ddl_command}
        ```

        Task:
        1. Analyze the DDL command and extract:
           - Table name
           - Columns, data types, primary keys, and constraints
        2. Generate a complete Java CRUD structure in the specified package with:
           - **Entity class** (with `@Entity`, `@Table`, proper JPA annotations, validation annotations like `@NotNull`, `@Size`, etc.)
           - **Repository interface** extending `JpaRepository`
           - **Wrapper/DTO class** (for external API exposure, mapping fields cleanly)
           - **Service class** (with CRUD methods and exception handling)
           - **Controller class** (REST endpoints for CRUD with `@RestController` and `@RequestMapping`)
        3. Follow best practices:
           - Use Lombok annotations (`@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`)
           - Ensure null-safety and input validation
           - Include standard HTTP responses (`ResponseEntity`, proper status codes)
           - Use constructor-based dependency injection
        4. Output Format:
           ```
           [Entity.java]
           <entity code>

           [Repository.java]
           <repository code>

           [Wrapper.java]
           <wrapper code>

           [Service.java]
           <service code>

           [Controller.java]
           <controller code>
           ```
        5. Do not include any explanations or extra commentary — only output as per the above structure.
        """

        response = get_chat_completion(prompt)
        output_file_name = "crud_api_generated.txt"
        output_file_path = os.path.join("/tmp", output_file_name)

        with open(output_file_path, "w") as output_file:
            output_file.write(response.strip())

        return output_file_path

    except MissingParameterException as e:
        return jsonify({'error': e.message}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
