// Auto-dismiss messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
  const msgs = document.querySelectorAll('.message');
  msgs.forEach(msg => {
    setTimeout(() => {
      msg.style.transition = 'opacity .5s';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 500);
    }, 4000);
  });

  // Set default due date to 14 days from issue date
  const issuedInput = document.querySelector('input[name="issued_date"]');
  const dueInput = document.querySelector('input[name="due_date"]');
  if (issuedInput && dueInput && !dueInput.value) {
    const due = new Date();
    due.setDate(due.getDate() + 14);
    dueInput.value = due.toISOString().split('T')[0];
  }
});
