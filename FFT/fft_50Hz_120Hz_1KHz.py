<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Ping Hsu 的互動履歷</title>
<link rel="stylesheet" href="css/style.css"/>
<script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>
</head>
<body>
<div class="wrap">

  <!-- 左側選單 -->
  <aside class="leftCol">
    <button data-target="intro" title="介紹">🏠</button>
    <button data-target="section1" title="Ping Resume">📄</button>
    <button data-target="section2" title="外部連結">🔗</button>
    <button data-target="chatbot" title="PingBot">🤖</button>
  </aside>

  <!-- 右側內容 -->
  <main class="rightCol">
    <section class="introCard" id="intro">
      <h2>歡迎來到 Ping Hsu 的網站！</h2>
      <p>今天是美好的一天，願你心情愉快！🌞</p>
    </section>

    <!-- Ping Resume 作品表格 -->
    <section class="sectionCard" id="section1">
      <h3>Ping Resume</h3>
      <p>作品連結與範例運行：</p>

      <table border="1" cellspacing="0" cellpadding="6">
        <thead>
          <tr>
            <th>作品名稱</th>
            <th>連結</th>
            <th>作品名稱</th>
            <th>連結</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Python</td>
            <td><a href="https://github.com/gsegria/python/tree/main/AI" target="_blank">打開網址</a></td>
            <td>Python FFT</td>
            <td><a href="https://github.com/gsegria/python/tree/main/FFT" target="_blank">打開網址</a></td>
          </tr>
          <tr>
            <td><button class="btn btn-black" onclick="runPython('print(\"Hello from Python AI\")')">運行範例</button></td>
            <td></td>
            <td><button class="btn btn-black" onclick="runPython('import numpy as np\nprint(np.fft.fft([1,2,3,4]))')">運行範例</button></td>
            <td></td>
          </tr>
          <tr>
            <td>XAMPP</td>
            <td><a href="https://github.com/gsegria/XAMPP_SQL" target="_blank">打開網址</a></td>
            <td>XAMPP SQL</td>
            <td><a href="https://github.com/gsegria/XAMPP_SQL" target="_blank">打開網址</a></td>
          </tr>
          <tr>
            <td><button class="btn btn-black" onclick="runPython('print(\"XAMPP example\")')">運行範例</button></td>
            <td></td>
            <td><button class="btn btn-black" onclick="runPython('print(\"XAMPP SQL example\")')">運行範例</button></td>
            <td></td>
          </tr>
        </tbody>
      </table>

      <h4>運行結果：</h4>
      <pre id="pyOutput" style="background:#f0f0f0;padding:10px;border-radius:5px;height:150px;overflow:auto;"></pre>
    </section>

    <!-- 外部連結 -->
    <section class="sectionCard" id="section2">
      <h3>外部連結</h3>
      <div class="buttons">
        <button class="btn btn-gradient" onclick="open104Home()">前往 104</button>
        <button class="btn btn-red" onclick="openPingHsu104()">前往 PingHsu's 104</button>
        <button class="btn btn-green" onclick="openLinkedIn()">前往 LinkedIn</button>
        <button class="btn btn-yellow" onclick="openLinkedInPingHsu()">前往 PingHsu's LinkedIn</button>
        <button class="btn btn-pink" onclick="openNotion()">前往 Notion</button>
      </div>
    </section>

    <!-- PingBot 聊天 -->
    <section class="sectionCard" id="chatbot">
      <h3>🤖 與 PingBot 聊聊 (未授權)</h3>
      <div id="chatbox"></div>
      <div class="chatControls">
        <input type="text" id="userInput" placeholder="輸入你的問題..." />
        <button class="btn btn-black" onclick="sendMessage()">送出</button>
        <button class="btn btn-gray" onclick="clearChat()">清除</button>
      </div>
    </section>
  </main>
</div>

<script src="js/main.js"></script>
<script src="js/chatbot.js"></script>

<script>
let pyodideReady = false;
let pyodide = null;

async function initPyodide() {
  pyodide = await loadPyodide();
  pyodideReady = true;
}
initPyodide();

async function runPython(code) {
  const outputEl = document.getElementById('pyOutput');
  if (!pyodideReady) {
    outputEl.textContent = 'Python 還沒準備好，請稍候...';
    return;
  }
  try {
    let result = await pyodide.runPythonAsync(code);
    outputEl.textContent = result ?? '';
  } catch (err) {
    outputEl.textContent = '錯誤：' + err;
  }
}
</script>
</body>
</html>
