# SBTI 测试（镜像）

地址：[https://sbti.unun.dev](https://sbti.unun.dev)  
原作者：[B站 蛋挞肉串儿](https://www.bilibili.com/video/BV1LpDHByET6/)

## 文案资源

站内文本统一集中在 [data/sbti-texts.js](D:/code/SBTI-test-main/data/sbti-texts.js)，包括：

- 首页和结果页提示语
- 全部题干和选项
- 全部人格简介
- 维度说明

`index.html` 只保留页面结构、样式和逻辑。

## Gemini 文案流程

当前项目参考 `D:\code\NovelVisualization\SwordComing` 的接法，使用：

- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `google-genai`

安装依赖：

```bash
pip install -r requirements-gemini.txt
```

### 正确的使用方式

这个脚本现在默认是“只填新增文案占位符”，不是“整份重写旧文案”。

- [data/sbti-texts.js](D:/code/SBTI-test-main/data/sbti-texts.js) 是锁定底稿
- 原题目、原选项、原人格描述不应该被 Gemini 改写
- 只有包含 `__GEMINI__` 的新增字符串才会送给 Gemini
- 如果 Gemini 改了任何非占位符旧文本，脚本会直接报错

新增文案请先写成这种形式：

```js
browseAll: '__GEMINI__: 首页按钮文案，意思是浏览所有人格，短一点，有梗，但别让人看不懂'
```

然后运行：

```bash
python scripts/run_sbti_texts_via_gemini.py
```

默认行为：

- 先生成候选稿到 `data/sbti-texts.gemini.js`
- 再自动同步到前端正在加载的 `data/sbti-texts.js`

如果你只想看候选稿，不想直接发到前端：

```bash
python scripts/run_sbti_texts_via_gemini.py --no-publish
```

如果你只想让 Gemini 在填“新增占位符文案”时，顺手参考 2025-2026 的中文互联网说法，避免写出翻译腔和假热梗，可以额外带：

```bash
python scripts/run_sbti_texts_via_gemini.py --ground-with-search
```

这个开关不会去碰原始旧文案，也不会默认全站重写；它只在占位符新文案生成时生效。

默认输入：

- `data/sbti-texts.js`

默认输出：

- `data/sbti-texts.gemini.js`

如果文件里没有 `__GEMINI__` 占位符，脚本会直接把输入原样复制到输出，不会调用 API。

提示词文件在：

- `prompts/sbti_texts_rewrite_system.txt`
- `prompts/sbti_texts_rewrite_pass.txt`
