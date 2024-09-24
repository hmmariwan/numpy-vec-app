from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Helper function to generate a random matrix
def create_matrix(rows, cols, min_val, max_val):
    return np.random.randint(min_val, max_val + 1, (rows, cols))

# Main page route to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and display results
@app.route('/result', methods=['POST'])
def result():
    try:
        # Get inputs from the form
        rows1 = int(request.form['rows1'])
        cols1 = int(request.form['cols1'])
        rows2 = int(request.form['rows2'])
        cols2 = int(request.form['cols2'])

        # Get min/max values for Matrix 1 and Matrix 2
        min_val1 = int(request.form['min_val1'])
        max_val1 = int(request.form['max_val1'])
        min_val2 = int(request.form['min_val2'])
        max_val2 = int(request.form['max_val2'])

        # Get the selected operation
        operation = request.form['operation']

        # Generate two random matrices using NumPy
        matrix1 = create_matrix(rows1, cols1, min_val1, max_val1)
        matrix2 = create_matrix(rows2, cols2, min_val2, max_val2)

        # Perform the selected operation
        if operation == "add":
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for addition!")
            result_matrix = matrix1 + matrix2

        elif operation == "subtract":
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for subtraction!")
            result_matrix = matrix1 - matrix2

        elif operation == "multiply":
            if cols1 != rows2:
                raise ValueError("Error: Matrix 1 columns must equal Matrix 2 rows for multiplication!")
            result_matrix = np.dot(matrix1, matrix2)

        elif operation == "divide":
            if matrix1.shape != matrix2.shape:
                raise ValueError("Error: Matrices must have the same dimensions for division!")
            result_matrix = np.divide(matrix1, matrix2, where=(matrix2 != 0))  # Avoid division by zero

        elif operation == "scalar":
            # Get the scalar value from the form
            scalar_value = float(request.form['scalar_value'])
            selected_matrix = request.form['matrix_select']  # Get the selected matrix

            if selected_matrix == "matrix1":
                result_matrix = matrix1 * scalar_value
            else:
                result_matrix = matrix2 * scalar_value

        # Render the result page with the matrices and the result of the operation
        return render_template('result.html',
                               matrix1=matrix1,
                               matrix2=matrix2,
                               result_matrix=result_matrix,
                               operation=operation)

    except Exception as e:
        # Handle any errors (such as invalid input) and display an error page
        return render_template('error.html', error=str(e))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
