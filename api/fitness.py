from flask import Flask, render_template
import markdown2

app = Flask(__name__)

@app.route('/')
def index():
    # Read the Markdown content from the file
    with open('fitness.md', 'r') as markdown_file:
        markdown_content = markdown_file.read()

    # Render the Markdown content to HTML
    html_content = markdown2.markdown(markdown_content)

    # Pass the HTML content to the template
    return render_template('index.html', html_content=html_content)

@app.route('/recommendation', methods=['POST'])
def get_recommendation():
    try:
        # Retrieve user inputs from the form
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        gender = request.form['gender']
        activity_level = request.form['activity_level']

        # Calculate BMI
        bmi = calculate_bmi(weight, height)

        # Determine fitness recommendation based on BMI and activity level
        recommendation = generate_recommendation(bmi, activity_level)

        return render_template('recommendation.html', recommendation=recommendation)

    except ValueError:
        error_message = "Invalid input. Please enter valid numerical values."
        return render_template('error.html', error_message=error_message)

def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

def generate_recommendation(bmi, activity_level):
    if bmi < 18.5:
        return "You are underweight. Consider increasing your calorie intake and doing strength training exercises."
    elif bmi < 25:
        if activity_level == 'sedentary':
            return "Your BMI is within the healthy range. Try to incorporate more physical activity into your daily routine."
        else:
            return "Your BMI is within the healthy range. Keep up the good work with your current activity level."
    else:
        return "You are overweight. Focus on a balanced diet and increase your physical activity level."

if __name__ == '__main__':
    app.run(debug=True)
