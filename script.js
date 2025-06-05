async function fetchIdeas(){
  const ul = document.getElementById('idea-list');
  ul.innerHTML = '';
  try{
    const res = await fetch('/ideas');
    const ideas = await res.json();
    if(ideas.length === 0){
      const li = document.createElement('li');
      li.textContent = 'アイデアはまだ登録されていません。';
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
  <input type="submit" value="完了"${item.done ? ' disabled':''}>`;
      form.addEventListener('submit', async (e)=>{
        e.preventDefault();
        const data = new URLSearchParams(new FormData(form));
        await fetch('/done', {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body:data});
        fetchIdeas();
      });
      li.appendChild(form);
      ul.appendChild(li);
    });
  }catch(err){
    const li = document.createElement('li');
    li.textContent = 'アイデアの読み込みに失敗しました。';
    ul.appendChild(li);
  }
}

function showMessage(msg, isError=false){
  const div = document.getElementById('message');
  div.textContent = msg;
  div.style.color = isError ? 'red' : 'green';
  setTimeout(()=>{ div.textContent = ''; }, 2000);
}

document.getElementById('add-form').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const form = e.target;
  const data = new URLSearchParams(new FormData(form));
  try{
    const res = await fetch('/add', {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body:data});
    if(!res.ok) throw new Error();
    showMessage('アイデアを追加しました。');
    form.reset();
  }catch(err){
    showMessage('アイデアの追加に失敗しました。', true);
  }
  document.getElementById('date').valueAsNumber = Date.now() - new Date().getTimezoneOffset()*60000;
  fetchIdeas();
});

document.addEventListener('DOMContentLoaded', ()=>{
  document.getElementById('date').valueAsNumber = Date.now() - new Date().getTimezoneOffset()*60000;
  fetchIdeas();
});
