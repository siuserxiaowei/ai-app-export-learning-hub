"use strict";

const pathSteps = [
  {
    number: "01",
    meta: "Day 1 / 30-60 分钟",
    title: "建立正确认知",
    body: "先读学习指南，理解出海不是翻译、AI 功能不等于产品、下载量不是最终指标。",
    href: "../docs/learning-guide.md"
  },
  {
    number: "02",
    meta: "Day 3 / 2 个案例起步",
    title: "拆一个可迁移案例",
    body: "从竞品学习册里选 2 个案例，回答它服务谁、替代了什么旧流程、为什么能收费。",
    href: "../docs/case-study-workbook.md"
  },
  {
    number: "03",
    meta: "Day 4-5 / 评分与收敛",
    title: "用评分表筛方向",
    body: "把候选方向放进 CSV 评分表，优先看 OPC 适配度、市场拉力、分发难度和合规风险。",
    href: "../data/opportunity-scorecard.csv"
  },
  {
    number: "04",
    meta: "Day 6-7 / 不写代码验证",
    title: "验证渠道与付费意愿",
    body: "按 7 天学习计划找到第一个低成本渠道，至少让 5 个目标用户看过你的方向假设。",
    href: "../docs/7-day-learning-plan.md"
  }
];

const caseTypes = {
  commerce: "电商/素材",
  content: "内容/视频",
  workflow: "文档/工作流",
  wellness: "健康/心理"
};

const cases = [
  {
    name: "Cal AI",
    type: "wellness",
    lesson: "把高频但麻烦的记录动作压缩成一次拍照。",
    avoid: "不要忽视准确性、健康合规和买量成本。"
  },
  {
    name: "Photoroom",
    type: "commerce",
    lesson: "不要做泛图片工具，要绑定卖货结果。",
    avoid: "不要一开始做完整设计平台。"
  },
  {
    name: "Gamma",
    type: "workflow",
    lesson: "用户买的是表达成果，不是 PPT 文件。",
    avoid: "不要做宽泛 PPT 生成器。"
  },
  {
    name: "PDF.ai / ChatPDF",
    type: "workflow",
    lesson: "文档是好入口，但要切行业文件流。",
    avoid: "不要再做泛 PDF Chat。"
  },
  {
    name: "HeyGen / Synthesia",
    type: "content",
    lesson: "视频本地化是真需求，企业愿意为省制作成本付费。",
    avoid: "不要做底层数字人平台。"
  },
  {
    name: "Lovart",
    type: "workflow",
    lesson: "Agent 是替用户完成一串专业决策。",
    avoid: "不要一开始做全能设计 Agent。"
  },
  {
    name: "Captions / CapCut",
    type: "content",
    lesson: "短视频要做平台、人群和任务。",
    avoid: "不要做泛剪辑器。"
  },
  {
    name: "Photo AI / Interior AI",
    type: "commerce",
    lesson: "可展示结果和创始人分发是 OPC 杠杆。",
    avoid: "不要只学一个人做产品，忽略分发资产。"
  },
  {
    name: "Calm / Wysa",
    type: "wellness",
    lesson: "情绪类产品卖的是信任、习惯和安全感。",
    avoid: "不要承诺治疗。"
  },
  {
    name: "ElevenLabs",
    type: "content",
    lesson: "底层能力可以成为别人工作流的基础设施。",
    avoid: "不要自己做底层语音模型。"
  }
];

const pathButtons = document.querySelectorAll(".path-step");
const pathNumber = document.querySelector("#pathNumber");
const pathMeta = document.querySelector("#pathMeta");
const pathTitle = document.querySelector("#pathTitle");
const pathBody = document.querySelector("#pathBody");
const pathLink = document.querySelector("#pathLink");
const caseGrid = document.querySelector("#caseGrid");
const caseCount = document.querySelector("#caseCount");
const filterButtons = document.querySelectorAll(".filter-button");
const copyButtons = document.querySelectorAll(".copy-button");

function setPressed(buttons, activeButton) {
  buttons.forEach(button => {
    const isActive = button === activeButton;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
}

function updatePath(stepIndex) {
  const step = pathSteps[stepIndex] || pathSteps[0];
  pathNumber.textContent = step.number;
  pathMeta.textContent = step.meta;
  pathTitle.textContent = step.title;
  pathBody.textContent = step.body;
  pathLink.href = step.href;
}

function makeCaseCard(item) {
  const card = document.createElement("article");
  card.className = "case-card";

  const tag = document.createElement("span");
  tag.className = "tag";
  tag.textContent = caseTypes[item.type] || item.type;

  const title = document.createElement("h3");
  title.textContent = item.name;

  const lesson = document.createElement("p");
  const lessonStrong = document.createElement("strong");
  lessonStrong.textContent = "学习：";
  lesson.append(lessonStrong, item.lesson);

  const avoid = document.createElement("p");
  const avoidStrong = document.createElement("strong");
  avoidStrong.textContent = "避开：";
  avoid.append(avoidStrong, item.avoid);

  card.append(tag, title, lesson, avoid);
  return card;
}

function renderCases(type = "all") {
  const visibleCases = type === "all" ? cases : cases.filter(item => item.type === type);
  caseGrid.replaceChildren(...visibleCases.map(makeCaseCard));
  caseCount.textContent = `显示 ${visibleCases.length} 个案例`;
}

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const helper = document.createElement("textarea");
  helper.value = text;
  helper.setAttribute("readonly", "");
  helper.style.position = "fixed";
  helper.style.top = "-999px";
  document.body.appendChild(helper);
  helper.select();
  document.execCommand("copy");
  helper.remove();
}

pathButtons.forEach(button => {
  button.addEventListener("click", () => {
    const stepIndex = Number(button.dataset.step || 0);
    setPressed(pathButtons, button);
    updatePath(stepIndex);
  });
});

filterButtons.forEach(button => {
  button.addEventListener("click", () => {
    setPressed(filterButtons, button);
    renderCases(button.dataset.filter || "all");
  });
});

copyButtons.forEach(button => {
  button.addEventListener("click", async () => {
    const target = document.querySelector(`#${button.dataset.copyTarget}`);
    if (!target) return;

    const defaultLabel = "复制模板";
    try {
      await copyText(target.textContent.trim());
      button.textContent = "已复制";
    } catch (error) {
      button.textContent = "复制失败";
    }

    window.setTimeout(() => {
      button.textContent = defaultLabel;
    }, 1600);
  });
});

renderCases();
