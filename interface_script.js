document.addEventListener('DOMContentLoaded', function() {
    const predictButton = document.getElementById('predict-button');
    const formContainer = document.getElementById('form-container');

    predictButton.addEventListener('click', function() {
        formContainer.classList.toggle('hidden');
    });

    const weightInput = document.getElementById('weight');
    const heightInput = document.getElementById('height');
    const bmiResult = document.getElementById('bmi-result');
    const bmiInput = document.getElementById('bmi');

    function calculateBMI() {
        const weight = parseFloat(weightInput.value);
        const height = parseFloat(heightInput.value) / 100;
        if (weight > 0 && height > 0) {
            const bmi = weight / (height * height);
            bmiResult.textContent = bmi.toFixed(2);
            bmiInput.value = bmi.toFixed(2);
        }
    }

    weightInput.addEventListener('input', calculateBMI);
    heightInput.addEventListener('input', calculateBMI);

    document.getElementById('begin-prediction-button').addEventListener('click', function() {
        // Show loading spinner
        document.getElementById('loading-spinner').style.display = 'block';
    });
});
