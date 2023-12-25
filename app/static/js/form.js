// Accessing buttons
const btmButton = document.querySelector('.btm-submit-btn');

// Accessing input fields
const fnameInput = document.querySelector('.fname-field');
const emailInput = document.querySelector('.email-field');
const pwdInput = document.querySelector('.pwd-field');

// Acessing First Name error/success messages
const fnameErrorMessage = document.querySelector('.fname-error-message');
const fnameSuccessMessage = document.querySelector('.fname-success-message');

// Accessing Email error/success messages
const emailErrorMessage = document.querySelector('.email-error-message');
const emailSuccessMessage = document.querySelector('.email-success-message');

// Accessing Password error/success messages
const pwdErrorMessage = document.querySelector('.pwd-error-message');
const pwdSuccessMessage = document.querySelector('.pwd-success-message');

const log = event => {
   const emailPattern = new RegExp("@");
   const emailResponse = emailPattern.test(emailInput.value);
   const pwdPattern = new RegExp("(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}");
   const pwdResponse = pwdPattern.test(pwdInput.value);
  
  // Conditions for first name
  if (fnameInput.value === '') {
    fnameErrorMessage.textContent = 'First Name cannot be empty';
    fnameErrorMessage.classList.add('error-txt');
    fnameInput.classList.add('failed');
    event.preventDefault();
  } 
  else {
    fnameSuccessMessage.textContent = 'First Name OK'
    fnameInput.classList.add('success');
    fnameErrorMessage.classList.add('success-txt');
    event.preventDefault();
  }
    
  // Condition for email address
  if (emailInput.value === '') {
    emailErrorMessage.textContent = 'Email Address cannot be empty';
    emailErrorMessage.classList.add('error-txt');
    emailInput.classList.add('failed');
    event.preventDefault();
  } else if (emailResponse === false) {
    emailErrorMessage.textContent = 'Looks like this is not an email';
    emailErrorMessage.classList.add('error-txt');
    emailInput.classList.add('failed');
    event.preventDefault();
  } else {
    emailSuccessMessage.textContent = 'Email OK';
    emailInput.classList.add('success');
    emailErrorMessage.classList.add('success-txt');
    event.preventDefault();
  }
  
  // Conditions for password
  if (pwdInput.value === '') {
    pwdErrorMessage.textContent = 'Password cannot be empty';
    pwdErrorMessage.classList.add('error-txt');
    pwdInput.classList.add('failed');
    event.preventDefault();
  } else if (pwdResponse === false ) {
    pwdErrorMessage.textContent = 'Password must include at least one digit, one lowercase letter, one uppercase letter, and be at least 8 characters long';
    pwdErrorMessage.classList.add('error-txt');
    pwdInput.classList.add('failed');
    event.preventDefault();
  } else {
    pwdSuccessMessage.textContent = 'Password OK';
    pwdInput.classList.add('success');
    pwdErrorMessage.classList.add('success-txt');
    event.preventDefault();
  }
}
