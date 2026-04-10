# SBTI 测试（镜像）

图片和html已拆分

地址：https://sbti.unun.dev  
原作者：[B站@蛆肉儿串儿](https://www.bilibili.com/video/BV1LpDHByET6/)

## 文案资源

站内文案已集中到 [data/sbti-texts.js](D:/code/SBTI-test-main/data/sbti-texts.js)，包括：

- 首页和结果页提示语
- 所有题干和选项
- 所有人格介绍
- 十五维度说明

`index.html` 现在只保留页面结构、样式和逻辑。

## Gemini 跑文案

当前项目参考 `D:\code\NovelVisualization\SwordComing` 的接法，使用：

- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `google-genai`

安装依赖：

```bash
pip install -r requirements-gemini.txt
```

配置环境变量后运行：

```bash
python scripts/run_sbti_texts_via_gemini.py
```

默认输入：

- `data/sbti-texts.js`

默认输出：

- `data/sbti-texts.gemini.js`

提示词文件在：

- `prompts/sbti_texts_rewrite_system.txt`
- `prompts/sbti_texts_rewrite_pass.txt`
