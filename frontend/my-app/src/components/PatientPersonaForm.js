import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import config from '../config';
import './PatientPersonaForm.css';

const PatientPersonaForm = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [errors, setErrors] = useState({});
  const [formData, setFormData] = useState({
    name: '',
    demographics: {
      age: '',
      sex: '',
      weight: '',
      height: '',
      ethnicity: '',
      occupation: ''
    },
    medicalHistory: {
      chronicConditions: '',
      previousSurgeries: '',
      hospitalizations: '',
      injuries: '',
      allergies: '',
      mentalHealthConditions: ''
    },
    medications: {
      current: '',
      dosages: '',
      past: '',
      interactions: ''
    },
    lifestyle: {
      diet: '',
      exercise: '',
      sleep: '',
      alcohol: '',
      tobacco: '',
      drugs: ''
    },
    familyHistory: {
      genetic: '',
      chronic: ''
    },
    immunization: {
      history: '',
      recent: '',
      travel: ''
    },
    symptoms: {
      primary: '',
      duration: '',
      severity: '',
      associated: '',
      painLevel: ''
    },
    vitals: {
      bloodPressure: '',
      heartRate: '',
      temperature: '',
      respiratoryRate: ''
    },
    testResults: {
      blood: '',
      imaging: '',
      urineStool: '',
      other: ''
    },
    allergiesSensitivities: {
      food: '',
      environmental: '',
      drug: ''
    },
    reproductive: {
      pregnancy: '',
      menstrual: '',
      contraception: '',
      fertility: ''
    },
    mentalHealth: {
      mood: '',
      memory: '',
      cognitive: '',
      stress: ''
    },
    social: {
      living: '',
      work: '',
      pets: ''
    },
    insurance: {
      status: '',
      facilities: '',
      interactions: ''
    }
  });

  // Field validation rules
  const validationRules = {
    name: {
      required: true,
      minLength: 2,
      pattern: /^[a-zA-Z\s-]+$/,
      message: 'Name must contain only letters, spaces, and hyphens'
    },
    demographics: {
      age: {
        required: true,
        type: 'number',
        min: 0,
        max: 150,
        message: 'Age must be between 0 and 150'
      },
      sex: {
        required: true,
        options: ['Male', 'Female'],
        message: 'Please select a valid sex'
      },
      weight: {
        required: true,
        pattern: /^\d+(\.\d{1,2})?\s*(lbs|kg)$/,
        message: 'Weight must be a number followed by lbs or kg (e.g., 150 lbs or 68 kg)'
      },
      height: {
        required: true,
        pattern: /^(\d{1,2}'\d{1,2}"|(\d+(\.\d{1,2})?\s*cm))$/,
        message: 'Height must be in format 5\'9" or 175 cm'
      }
    },
    vitals: {
      bloodPressure: {
        pattern: /^\d{2,3}\/\d{2,3}\s*mmHg$/,
        message: 'Blood pressure must be in format 120/80 mmHg'
      },
      heartRate: {
        pattern: /^\d{2,3}$/,
        message: 'Heart rate must be a number between 0-999'
      },
      temperature: {
        pattern: /^\d{2,3}(\.\d)?\s*(F|C)$/,
        message: 'Temperature must be in format 98.6F or 37C'
      },
      respiratoryRate: {
        pattern: /^\d{1,2}$/,
        message: 'Respiratory rate must be a number between 0-99'
      }
    },
    symptoms: {
      painLevel: {
        pattern: /^([0-9]|10)\/10$/,
        message: 'Pain level must be in format 5/10 (0-10)'
      }
    }
  };

  const validateField = (section, field, value) => {
    let error = '';
    let rules = section === 'name' 
      ? validationRules[section]
      : validationRules[section]?.[field];

    if (!rules) return '';

    if (rules.required && !value) {
      return 'This field is required';
    }

    if (rules.type === 'number') {
      const num = Number(value);
      if (isNaN(num)) {
        return 'Must be a number';
      }
      if (rules.min !== undefined && num < rules.min) {
        return `Must be at least ${rules.min}`;
      }
      if (rules.max !== undefined && num > rules.max) {
        return `Must be less than ${rules.max}`;
      }
    }

    if (rules.options && !rules.options.includes(value)) {
      return rules.message;
    }

    if (rules.pattern && !rules.pattern.test(value)) {
      return rules.message;
    }

    if (rules.minLength && value.length < rules.minLength) {
      return `Must be at least ${rules.minLength} characters`;
    }

    return '';
  };

  const formatFieldName = (name) => {
    return name
      .replace(/([A-Z])/g, ' $1')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const handleInputChange = (section, field, value) => {
    // Update form data
    if (section === 'name') {
      setFormData(prev => ({
        ...prev,
        name: value
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [section]: {
          ...prev[section],
          [field]: value
        }
      }));
    }

    // Validate and update errors
    const error = validateField(section, field, value);
    setErrors(prev => ({
      ...prev,
      [section]: {
        ...prev?.[section],
        [field]: error
      }
    }));
  };

  const getInputType = (section, field) => {
    if (section === 'demographics' && field === 'age') return 'number';
    return 'text';
  };

  const renderFormField = (sectionName, fieldName, value) => {
    const error = errors[sectionName]?.[fieldName];
    const rules = validationRules[sectionName]?.[fieldName];

    if (rules?.options) {
      return (
        <div className={`form-field ${error ? 'error' : ''}`}>
          <label>{formatFieldName(fieldName)}:</label>
          <select
            value={value}
            onChange={(e) => handleInputChange(sectionName, fieldName, e.target.value)}
            className={error ? 'error' : ''}
          >
            <option value="">Select {formatFieldName(fieldName)}</option>
            {rules.options.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
          {error && <div className="error-message">{error}</div>}
        </div>
      );
    }

    return (
      <div className={`form-field ${error ? 'error' : ''}`}>
        <label>{formatFieldName(fieldName)}:</label>
        <input
          type={getInputType(sectionName, fieldName)}
          value={value}
          onChange={(e) => handleInputChange(sectionName, fieldName, e.target.value)}
          placeholder={`Enter ${formatFieldName(fieldName)}`}
          className={error ? 'error' : ''}
          min={rules?.min}
          max={rules?.max}
        />
        {error && <div className="error-message">{error}</div>}
      </div>
    );
  };

  const renderFormSection = (sectionName, fields) => {
    return (
      <div className="form-section">
        <h3>{formatFieldName(sectionName)}</h3>
        {Object.entries(fields).map(([fieldName, value]) => (
          renderFormField(sectionName, fieldName, value)
        ))}
      </div>
    );
  };

  const renderStep = () => {
    switch(currentStep) {
      case 1:
        return (
          <div className="form-section">
            <h3>Basic Information</h3>
            {renderFormField('name', 'name', formData.name)}
            {renderFormSection('demographics', formData.demographics)}
          </div>
        );
      case 2:
        return renderFormSection('medicalHistory', formData.medicalHistory);
      case 3:
        return renderFormSection('medications', formData.medications);
      case 4:
        return renderFormSection('lifestyle', formData.lifestyle);
      case 5:
        return renderFormSection('familyHistory', formData.familyHistory);
      case 6:
        return renderFormSection('immunization', formData.immunization);
      case 7:
        return renderFormSection('symptoms', formData.symptoms);
      case 8:
        return renderFormSection('vitals', formData.vitals);
      case 9:
        return renderFormSection('testResults', formData.testResults);
      case 10:
        return renderFormSection('allergiesSensitivities', formData.allergiesSensitivities);
      case 11:
        return renderFormSection('reproductive', formData.reproductive);
      case 12:
        return renderFormSection('mentalHealth', formData.mentalHealth);
      case 13:
        return renderFormSection('social', formData.social);
      case 14:
        return renderFormSection('insurance', formData.insurance);
      default:
        return null;
    }
  };

  const validateStep = (step) => {
    let stepErrors = {};
    
    const validateSection = (section) => {
      if (section === 'name') {
        const error = validateField('name', null, formData.name);
        if (error) stepErrors.name = error;
      } else {
        Object.entries(formData[section]).forEach(([field, value]) => {
          const error = validateField(section, field, value);
          if (error) {
            stepErrors[section] = {
              ...stepErrors[section],
              [field]: error
            };
          }
        });
      }
    };

    switch(step) {
      case 1:
        validateSection('name');
        validateSection('demographics');
        break;
      case 2:
        validateSection('medicalHistory');
        break;
      // Add validation for other steps as needed
    }

    setErrors(stepErrors);
    return Object.keys(stepErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handleSubmit = async () => {
    if (!validateStep(currentStep)) {
      return;
    }

    try {
      const response = await fetch(`${config.apiUrl}/api/save-persona`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          data: formData
        }),
      });

      if (response.ok) {
        const result = await response.json();
        alert('Patient persona saved successfully!');
        console.log('Saved to:', result.file_path);
        // Reset form
        setFormData({
          name: '',
          demographics: { age: '', sex: '', weight: '', height: '', ethnicity: '', occupation: '' },
          medicalHistory: { chronicConditions: '', previousSurgeries: '', hospitalizations: '', injuries: '', allergies: '', mentalHealthConditions: '' },
          medications: { current: '', dosages: '', past: '', interactions: '' },
          lifestyle: { diet: '', exercise: '', sleep: '', alcohol: '', tobacco: '', drugs: '' },
          familyHistory: { genetic: '', chronic: '' },
          immunization: { history: '', recent: '', travel: '' },
          symptoms: { primary: '', duration: '', severity: '', associated: '', painLevel: '' },
          vitals: { bloodPressure: '', heartRate: '', temperature: '', respiratoryRate: '' },
          testResults: { blood: '', imaging: '', urineStool: '', other: '' },
          allergiesSensitivities: { food: '', environmental: '', drug: '' },
          reproductive: { pregnancy: '', menstrual: '', contraception: '', fertility: '' },
          mentalHealth: { mood: '', memory: '', cognitive: '', stress: '' },
          social: { living: '', work: '', pets: '' },
          insurance: { status: '', facilities: '', interactions: '' }
        });
        setCurrentStep(1);
        setErrors({});
        // Navigate back to home page
        navigate('/');
      } else {
        const errorData = await response.json();
        alert(`Error saving patient persona: ${errorData.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error saving patient persona: ' + error.message);
    }
  };

  const totalSteps = 14;

  return (
    <div className="patient-persona-form">
      <h2>Create Patient Persona</h2>
      <div className="progress-bar">
        Step {currentStep} of {totalSteps}
      </div>
      
      {renderStep()}
      
      <div className="form-navigation">
        {currentStep > 1 && (
          <button onClick={() => setCurrentStep(prev => prev - 1)}>
            Previous
          </button>
        )}
        {currentStep < totalSteps ? (
          <button onClick={handleNext}>
            Next
          </button>
        ) : (
          <button onClick={handleSubmit}>Submit</button>
        )}
      </div>
    </div>
  );
};

export default PatientPersonaForm;
