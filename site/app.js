const cases = [
  { name: "Cal AI", type: "wellness", lesson: "把高频但麻烦的记录动作压缩成一次拍照。", avoid: "不要忽视准确性、健康合规和买量成本。" },
  { name: "Photoroom", type: "commerce", lesson: "不要做泛图片工具，要绑定卖货结果。", avoid: "不要一开始做完整设计平台。" },
  { name: "Gamma", type: "workflow", lesson: "用户买的是表达成果，不是 PPT 文件。", avoid: "不要做宽泛 PPT 生成器。" },
  { name: "PDF.ai / ChatPDF", type: "workflow", lesson: "文档是好入口，但要切行业文件流。", avoid: "不要再做泛 PDF Chat。" },
  { name: "HeyGen / Synthesia", type: "content", lesson: "视频本地化是真需求，企业愿意为省制作成本付费。", avoid: "不要做底层数字人平台。" },
  { name: "Lovart", type: "workflow", lesson: "Agent 是替用户完成一串专业决策。", avoid: "不要一开始做全能设计 Agent。" },
  { name: "Captions / CapCut", type: "content", lesson: "短视频要做平台 + 人群 + 任务。", avoid: "不要做泛剪辑器。" },
  { name: "Photo AI / Interior AI", type: "commerce", lesson: "可展示结果和创始人分发是 OPC 杠杆。", avoid: "不要只学一个人做产品，忽略分发资产。" },
  { name: "Calm / Wysa", type: "wellness", lesson: "情绪类产品卖的是信任、习惯和安全感。", avoid: "不要承诺治疗。" },
  { name: "ElevenLabs", type: "content", lesson: "底层能力可以成为别人工作流的基础设施。", avoid: "不要自己做底层语音模型。" }
];

const grid = document.querySelector("#caseGrid");
const filter = document.querySelector("#caseFilter");

function renderCases(type = "all") {
  const visible = type === "all" ? cases : cases.filter(item => item.type === type);
  grid.innerHTML = visible.map(item => `
    <article>
      <div class="tag">${item.type}</div>
      <h3>${item.name}</h3>
      <p><strong>学习：</strong>${item.lesson}</p>
      <p><strong>避开：</strong>${item.avoid}</p>
    </article>
  `).join("");
}

filter.addEventListener("change", event => renderCases(event.target.value));
renderCases();

