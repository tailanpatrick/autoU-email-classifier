const form = document.getElementById('emailForm');
const resultDiv = document.getElementById('result');
const categoryP = document.getElementById('category');
const responseP = document.getElementById('response');
const loadingDiv = document.getElementById('loading');
const fileInput = document.getElementById('fileInput');
const emailInput = document.getElementById('emailInput');
const removeBtn = document.getElementById('removeBtn');
const errorDiv = document.getElementById('error');

fileInput.addEventListener('change', () => {
	if (fileInput.files.length > 0) {
		removeBtn.classList.remove('hidden');
	} else {
		removeBtn.classList.add('hidden');
	}
});

removeBtn.addEventListener('click', () => {
	fileInput.value = '';
	removeBtn.classList.add('hidden');
	showError('');
});

form.addEventListener('submit', async (e) => {
	e.preventDefault();
	errorDiv.classList.add('hidden');
	resultDiv.classList.add('hidden');
	loadingDiv.classList.remove('hidden');
	responseP.innerHTML = '';

	const formData = new FormData();
	if (fileInput.files.length > 0) {
		const file = fileInput.files[0];
		if (file.type !== 'application/pdf' && file.type !== 'text/plain') {
			showError('Formato de arquivo inválido! Use .txt ou .pdf');

			loadingDiv.classList.add('hidden');
			return;
		}
		formData.append('file', file);
	}

	formData.append('text', emailInput.value);

	try {
		const response = await fetch(
			'http://192.168.100.175:8000/process-email',
			{
				method: 'POST',
				body: formData,
			}
		);

		const data = await response.json();

		if (!response.ok) {
			showError(data.detail || data.detail);
			return;
		}

		categoryP.textContent = data.categoria;
		animateTyping(data.resposta);
		resultDiv.classList.remove('hidden');
	} catch (err) {
		showError(err.message);
	} finally {
		loadingDiv.classList.add('hidden');
	}
});

function showError(message) {
	errorDiv.textContent = message;
	errorDiv.classList.remove('hidden');
}

function animateTyping(text) {
	responseP.innerHTML = '';
	text.split('').forEach((char, i) => {
		const span = document.createElement('span');
		span.textContent = char;
		span.style.animationDelay = `${i * 0.03}s`;
		responseP.appendChild(span);
	});
}
