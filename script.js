async function fetchIdeas(){
  const res = await fetch('/ideas');
  const ideas = await res.json();
  const ul = document.getElementById('idea-list');
  ul.innerHTML = '';
  if(ideas.length === 0){
    const li = document.createElement('li');
    li.textContent = 'No ideas recorded.';
    ul.appendChild(li);
    return;
  }
  ideas.forEach((item, idx)=>{
    const li = document.createElement('li');
    if(item.done) li.classList.add('done');
    li.textContent = `${item.idea} [${item.date || '-'}] (${item.done ? '✓':'x'})`;
    const form = document.createElement('form');
    form.className = 'inline';
    form.innerHTML = `<input type="hidden" name="idx" value="${idx}">
<input type="submit" value="Mark done"${item.done ? ' disabled':''}>`;
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const data = new URLSearchParams(new FormData(form));
      await fetch('/done', {method:'POST', body:data});
      fetchIdeas();
    });
    li.appendChild(form);
    ul.appendChild(li);
  });
}

document.getElementById('add-form').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const form = e.target;
  const data = new URLSearchParams(new FormData(form));
  await fetch('/add', {method:'POST', body:data});
  form.reset();
  document.getElementById('date').valueAsNumber = Date.now() - new Date().getTimezoneOffset()*60000;
  fetchIdeas();
});

document.addEventListener('DOMContentLoaded', ()=>{
  document.getElementById('date').valueAsNumber = Date.now() - new Date().getTimezoneOffset()*60000;
  fetchIdeas();
});
