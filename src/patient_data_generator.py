import os
from chatgpt_client import ChatGPTClient

SYSTEM_PROMPT = """
You are a medical data generator who will be provided with a taxonomy and you will generate data for that taxonomy.
The data should represent patients in real life. You will be called multiple times, so be creative with your responses.

Taxonomy:

1. Basic Demographics:
- Age
- Sex
- Weight
- Height
- Ethnicity
- Occupation (if relevant to health risks)

2. Medical History:
- Chronic conditions (e.g., diabetes, hypertension, heart disease)
- Previous surgeries
- Hospitalizations
- Injuries
- Allergies (especially drug, food, or environmental allergies)
- Mental health conditions (e.g., depression, anxiety)

3. Medication Details:
- Current medications (prescriptions, over-the-counter, supplements)
- Dosages and frequency
- Past medications (recently discontinued drugs)
- Drug interactions or known sensitivities

4. Lifestyle Factors:
- Dietary habits (vegetarian, vegan, keto, etc.)
- Exercise routine (frequency, type of exercise)
- Sleep patterns (hours per night, sleep quality)
- Alcohol use
- Tobacco use
- Recreational drug use

5. Family Medical History:
- Genetic conditions (e.g., cancer, cardiovascular diseases)
- Family history of chronic illnesses

6. Immunization Status:
- Vaccination history (especially for conditions like flu, tetanus, COVID-19, etc.)
- Recent vaccinations
- Travel history and vaccines related to travel

7. Symptoms/Presenting Concerns:
- Primary complaint (e.g., headache, fever, stomach pain)
- Duration of symptoms
- Severity of symptoms
- Associated symptoms (e.g., nausea, dizziness)
- Pain level (if applicable)

8. Vital Signs:
- Blood pressure
- Heart rate
- Body temperature
- Respiratory rate

9. Test Results:
- Recent blood tests
- Imaging results (e.g., X-rays, MRIs)
- Urine/stool analysis
- Other diagnostic results

10. Allergies/Sensitivities:
- Food allergies
- Environmental allergens (e.g., pollen, dust)
- Drug allergies

11. Reproductive Health (if relevant):
- Pregnancy status
- Menstrual cycle details
- Contraception use
- Fertility concerns

12. Mental and Cognitive Health:
- Mood changes
- Memory issues
- Cognitive impairments
- Stress and anxiety levels

13. Social and Environmental Factors:
- Living conditions (e.g., living alone, crowded environment)
- Work environment (e.g., exposure to chemicals, stress level)
- Pets (for zoonotic disease risk)

14. Insurance and Healthcare Preferences:
- Insurance status
- Preferred healthcare facilities
- Past interactions with healthcare systems

Your output should follow the format provided in the taxonomy.
"""

def main():
    client = ChatGPTClient()
    client.set_system_prompt(SYSTEM_PROMPT)
    response = client.get_response("Generate a patient data for a male who works in mining and has an associated disease due to his profession")

    print(response)

    patient_dir = '../patient_persona'
    if not os.path.exists(patient_dir):
        os.makedirs(patient_dir)

    existing_files = [f for f in os.listdir(patient_dir) if f.startswith('patient_') and f.endswith('.txt')]
    if not existing_files:
        last_index = 0
    else:
        last_index = max([int(f.split('_')[1].split('.')[0]) for f in existing_files])

    new_index = last_index + 1
    with open(os.path.join(patient_dir, f'patient_{new_index}.txt'), 'w') as file:
        file.write(response)


if __name__ == '__main__':
    main()

