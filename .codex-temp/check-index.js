
    const texts = window.SBTI_TEXTS;
    if (!texts) {
      throw new Error('Missing window.SBTI_TEXTS from data/sbti-texts.js');
    }
    const uiText = texts.ui;
    const dimensionMeta = texts.dimensionMeta;
    const questions = texts.questions;
    const specialQuestions = texts.specialQuestions;
    const TYPE_LIBRARY = texts.typeLibrary;
    const COMPATIBILITY_TEXT = texts.compatibilityText || {};
    const TYPE_IMAGES = {
  "IMSB": "./image/IMSB.png",
  "BOSS": "./image/BOSS.png",
  "MUM": "./image/MUM.png",
  "FAKE": "./image/FAKE.png",
  "Dior-s": "./image/Dior-s.jpg",
  "DEAD": "./image/DEAD.png",
  "ZZZZ": "./image/ZZZZ.png",
  "GOGO": "./image/GOGO.png",
  "FUCK": "./image/FUCK.png",
  "CTRL": "./image/CTRL.png",
  "HHHH": "./image/HHHH.png",
  "SEXY": "./image/SEXY.png",
  "OJBK": "./image/OJBK.png",
  "JOKE-R": "./image/JOKE-R.jpg",
  "POOR": "./image/POOR.png",
  "OH-NO": "./image/OH-NO.png",
  "MONK": "./image/MONK.png",
  "SHIT": "./image/SHIT.png",
  "THAN-K": "./image/THAN-K.png",
  "MALO": "./image/MALO.png",
  "ATM-er": "./image/ATM-er.png",
  "THIN-K": "./image/THIN-K.png",
  "SOLO": "./image/SOLO.png",
  "LOVE-R": "./image/LOVE-R.png",
  "WOC!": "./image/WOC.png",
  "DRUNK": "./image/DRUNK.png",
  "IMFW": "./image/IMFW.png"
};

    const NORMAL_TYPES = [
  {
    "code": "CTRL",
    "pattern": "HHH-HMH-MHH-HHH-MHM"
  },
  {
    "code": "ATM-er",
    "pattern": "HHH-HHM-HHH-HMH-MHL"
  },
  {
    "code": "Dior-s",
    "pattern": "MHM-MMH-MHM-HMH-LHL"
  },
  {
    "code": "BOSS",
    "pattern": "HHH-HMH-MMH-HHH-LHL"
  },
  {
    "code": "THAN-K",
    "pattern": "MHM-HMM-HHM-MMH-MHL"
  },
  {
    "code": "OH-NO",
    "pattern": "HHL-LMH-LHH-HHM-LHL"
  },
  {
    "code": "GOGO",
    "pattern": "HHM-HMH-MMH-HHH-MHM"
  },
  {
    "code": "SEXY",
    "pattern": "HMH-HHL-HMM-HMM-HLH"
  },
  {
    "code": "LOVE-R",
    "pattern": "MLH-LHL-HLH-MLM-MLH"
  },
  {
    "code": "MUM",
    "pattern": "MMH-MHL-HMM-LMM-HLL"
  },
  {
    "code": "FAKE",
    "pattern": "HLM-MML-MLM-MLM-HLH"
  },
  {
    "code": "OJBK",
    "pattern": "MMH-MMM-HML-LMM-MML"
  },
  {
    "code": "MALO",
    "pattern": "MLH-MHM-MLH-MLH-LMH"
  },
  {
    "code": "JOKE-R",
    "pattern": "LLH-LHL-LML-LLL-MLM"
  },
  {
    "code": "WOC!",
    "pattern": "HHL-HMH-MMH-HHM-LHH"
  },
  {
    "code": "THIN-K",
    "pattern": "HHL-HMH-MLH-MHM-LHH"
  },
  {
    "code": "SHIT",
    "pattern": "HHL-HLH-LMM-HHM-LHH"
  },
  {
    "code": "ZZZZ",
    "pattern": "MHL-MLH-LML-MML-LHM"
  },
  {
    "code": "POOR",
    "pattern": "HHL-MLH-LMH-HHH-LHL"
  },
  {
    "code": "MONK",
    "pattern": "HHL-LLH-LLM-MML-LHM"
  },
  {
    "code": "IMSB",
    "pattern": "LLM-LMM-LLL-LLL-MLM"
  },
  {
    "code": "SOLO",
    "pattern": "LML-LLH-LHL-LML-LHM"
  },
  {
    "code": "FUCK",
    "pattern": "MLL-LHL-LLM-MLL-HLH"
  },
  {
    "code": "DEAD",
    "pattern": "LLL-LLM-LML-LLL-LHM"
  },
  {
    "code": "IMFW",
    "pattern": "LLH-LHL-LML-LLL-MLL"
  }
    ];
    const EASTER_EGG_TYPES = ['HHHH', 'DRUNK'];
    const BROWSE_GROUPS = [
      {
        watermark: 'CONTROL',
        title: '控场派',
        kicker: '不抓方向盘就开始浑身难受',
        desc: '嘴上像在提建议，实际已经把场子接过去了。你这边还在想，ta那边连流程、预算和情绪都替你排完了。',
        theme: 'plum',
        codes: ['CTRL', 'ATM-er', 'BOSS', 'GOGO', 'THIN-K']
      },
      {
        watermark: 'DRAMA',
        title: '关系病',
        kicker: '想被爱，也想把爱演成连续剧',
        desc: '一边想被懂，一边把关系过成连续剧。聊天记录像病历，情绪起伏像天气预报，天天都有新剧情。',
        theme: 'mint',
        codes: ['THAN-K', 'OH-NO', 'LOVE-R', 'MUM', 'SOLO']
      },
      {
        watermark: 'CIRCUS',
        title: '节目组',
        kicker: '人生烂成这样，总得整点效果',
        desc: '发光、装蒜、发癫、整活，全都能来一点。别人忙着过日子，ta忙着给自己加机位。',
        theme: 'peach',
        codes: ['Dior-s', 'SEXY', 'FAKE', 'JOKE-R', 'WOC!']
      },
      {
        watermark: 'AFK',
        title: '挂机区',
        kicker: '肉身在线，灵魂下线',
        desc: '主打一个人还在线，魂先下班。能少动一步算一步，能少受一点罪算一点，世界末日来了也想先睡醒再说。',
        theme: 'sky',
        codes: ['ZZZZ', 'MONK', 'POOR', 'DEAD', 'OJBK']
      },
      {
        watermark: 'WRECK',
        title: '烂命局',
        kicker: '骂世界，顺手再骂自己',
        desc: '怒气、废气、丧气搅成一锅，活着像开一台随时会散架的破机器。话是难听了点，但确实比鸡汤像人话。',
        theme: 'sage',
        codes: ['SHIT', 'FUCK', 'IMSB', 'IMFW', 'MALO']
      }
    ];
    const DIM_EXPLANATIONS = texts.dimExplanations;
    const dimensionOrder = ['S1','S2','S3','E1','E2','E3','A1','A2','A3','Ac1','Ac2','Ac3','So1','So2','So3'];
    const NORMAL_TYPE_CODES = NORMAL_TYPES.map(type => type.code);
    const COMPATIBILITY_RULES = {
      friendship: {
        weights: {
          S1: ['same', 1.0], S2: ['same', 1.0], S3: ['same', 0.9],
          E1: ['same', 1.0], E2: ['adjacent', 0.8], E3: ['same', 1.0],
          A1: ['same', 1.1], A2: ['same', 1.1], A3: ['same', 1.0],
          Ac1: ['adjacent', 0.8], Ac2: ['adjacent', 0.9], Ac3: ['adjacent', 0.8],
          So1: ['adjacent', 0.9], So2: ['same', 1.0], So3: ['adjacent', 0.8]
        },
        reasonLabels: {
          S1: '自尊系统差不多',
          S2: '脑回路能对上频',
          S3: '想要的东西不太打架',
          E1: '安全感节奏接得住',
          E2: '情绪浓度能互相消化',
          E3: '边界感不至于互踩',
          A1: '看世界的滤镜差不多',
          A2: '规矩和松紧能对上',
          A3: '人生观不会天天打架',
          Ac1: '做事冲劲能接上',
          Ac2: '拍板节奏还算合拍',
          Ac3: '执行习惯不容易互拖',
          So1: '一个能拉一个出门',
          So2: '熟络距离不容易越线',
          So3: '说话方式还听得懂'
        }
      },
      romantic: {
        weights: {
          S1: ['same', 0.9], S2: ['same', 1.0], S3: ['same', 0.8],
          E1: ['same', 1.3], E2: ['adjacent', 1.0], E3: ['adjacent', 1.2],
          A1: ['same', 0.9], A2: ['adjacent', 0.8], A3: ['same', 1.0],
          Ac1: ['adjacent', 0.8], Ac2: ['adjacent', 0.9], Ac3: ['adjacent', 0.8],
          So1: ['adjacent', 0.9], So2: ['adjacent', 1.0], So3: ['same', 1.0]
        },
        reasonLabels: {
          S1: '自尊系统不容易互伤',
          S2: '自我认知还算对得上',
          S3: '未来想法没差到离谱',
          E1: '安全感频道对上了',
          E2: '情绪投入能接得住',
          E3: '黏与不黏还能商量',
          A1: '看人的方式差不多',
          A2: '关系规矩不至于打架',
          A3: '人生意义感还能接轨',
          Ac1: '推进关系的劲头能配上',
          Ac2: '吵架拍板不容易失控',
          Ac3: '过日子的手脚能配合',
          So1: '社交出场方式能互补',
          So2: '亲密距离感还算合拍',
          So3: '表达方式不至于鸡同鸭讲'
        }
      }
    };
    const COMPATIBILITY_SPECIAL_MATCHES = {
      friendship: {
        HHHH: {
          code: 'JOKE-R',
          score: 78,
          topReasons: ['气氛越烂越能玩起来', '废话密度能对上', '正常人本来也进不来你们频道']
        },
        DRUNK: {
          code: 'JOKE-R',
          score: 81,
          topReasons: ['一个喝高了一个接梗', '现场再烂都能硬聊下去', '丢人这件事你们谁也别嫌谁']
        }
      },
      romantic: {
        HHHH: {
          code: 'LOVE-R',
          score: 69,
          topReasons: ['一个瞎乐一个瞎爱', '沉重和轻飘正好互撞', '关系能甜一阵也能炸很快']
        },
        DRUNK: {
          code: 'LOVE-R',
          score: 73,
          topReasons: ['一个借酒发疯一个真情泛滥', '夜里都很会制造情绪高潮', '白天收拾残局时也一样惨']
        }
      }
    };

    const DRUNK_TRIGGER_QUESTION_ID = 'drink_gate_q2';

    const app = {
      shuffledQuestions: [],
      answers: {},
      previewMode: false,
      resultViewMode: 'test'
    };

    const screens = {
      intro: document.getElementById('intro'),
      browse: document.getElementById('browse'),
      test: document.getElementById('test'),
      result: document.getElementById('result')
    };

    const questionList = document.getElementById('questionList');
    const browseMainGrid = document.getElementById('browseMainGrid');
    const browseEasterGrid = document.getElementById('browseEasterGrid');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const submitBtn = document.getElementById('submitBtn');
    const restartBtn = document.getElementById('restartBtn');
    const resultBrowseBtn = document.getElementById('resultBrowseBtn');
    const testHint = document.getElementById('testHint');
    const posterImage = document.getElementById('posterImage');
    const posterCaption = document.getElementById('posterCaption');
    const resultModeKicker = document.getElementById('resultModeKicker');
    const resultTypeName = document.getElementById('resultTypeName');
    const matchBadge = document.getElementById('matchBadge');
    const resultTypeSub = document.getElementById('resultTypeSub');
    const resultDesc = document.getElementById('resultDesc');
    const funNote = document.getElementById('funNote');
    const dimBox = document.getElementById('dimBox');
    const authorContent = document.getElementById('authorContent');

    function formatText(template, values) {
      return template.replace(/\{(\w+)\}/g, (_, key) => String(values[key] ?? ''));
    }

    function applyStaticTexts() {
      document.title = uiText.pageTitle;
      document.getElementById('introTitle').textContent = uiText.introTitle;
      document.getElementById('startBtn').textContent = uiText.buttons.start;
      document.getElementById('browseBtn').textContent = uiText.buttons.browseAll;
      document.getElementById('randomBtn').textContent = uiText.buttons.randomResult;
      document.getElementById('backIntroBtn').textContent = uiText.buttons.backIntro;
      document.getElementById('submitBtn').textContent = uiText.buttons.submit;
      restartBtn.textContent = uiText.buttons.restart;
      resultBrowseBtn.textContent = uiText.buttons.browseAll;
      document.getElementById('toTopBtn').textContent = uiText.buttons.toTop;
      document.getElementById('browseBackBtn').textContent = uiText.buttons.backIntro;
      document.getElementById('browseStartBtn').textContent = uiText.buttons.start;

      document.getElementById('browseTitle').textContent = uiText.browse.title;
      document.getElementById('browseSub').textContent = uiText.browse.sub;
      document.getElementById('browseMainTitle').textContent = uiText.browse.mainTitle;
      document.getElementById('browseMainSub').textContent = uiText.browse.mainSub;
      document.getElementById('browseEasterTitle').textContent = uiText.browse.easterTitle;
      document.getElementById('browseEasterSub').textContent = uiText.browse.easterSub;

      document.getElementById('introAuthorLabel').textContent = uiText.introMeta.authorLabel;
      document.getElementById('introAuthorLink').textContent = uiText.introMeta.authorLinkText;
      document.getElementById('introHostLabel').textContent = uiText.introMeta.hostLabel;
      document.getElementById('introHostValue').textContent = uiText.introMeta.hostValue;
      document.getElementById('introDomainLabel').textContent = uiText.introMeta.domainLabel;
      document.getElementById('introDomainValue').textContent = uiText.introMeta.domainValue;

      progressText.textContent = uiText.progress.initial;
      testHint.textContent = uiText.progress.incompleteHint;

      posterImage.alt = uiText.result.posterAlt;
      posterCaption.textContent = uiText.result.posterCaptionDefault;
      resultModeKicker.textContent = uiText.result.modeKickerDefault;
      resultTypeName.textContent = uiText.result.typeNameDefault;
      matchBadge.textContent = uiText.result.matchBadgeDefault;
      resultTypeSub.textContent = uiText.result.typeSubDefault;
      document.getElementById('analysisTitle').textContent = uiText.result.analysisTitle;
      document.getElementById('dimTitle').textContent = uiText.result.dimTitle;
      document.getElementById('noteTitle').textContent = uiText.result.noteTitle;
      funNote.textContent = uiText.result.noteDefault;
      document.getElementById('authorSummary').textContent = uiText.result.authorSummary;
      document.documentElement.style.setProperty('--author-summary-expand', `"${uiText.result.authorExpand}"`);
      document.documentElement.style.setProperty('--author-summary-collapse', `"${uiText.result.authorCollapse}"`);
      authorContent.innerHTML = uiText.result.authorParagraphs.map(text => `<p>${text}</p>`).join('');

      const detailUI = uiText.detail || {};
      const navTitle = isPlaceholder(detailUI.navTitle) ? '这人什么路数' : detailUI.navTitle;
      document.getElementById('detailNavTitle').textContent = navTitle;
      const navIntro = detailUI.navIntro || '先看概况';
      const navRomantic = detailUI.navRomantic || '谈恋爱时';
      const navFriends = detailUI.navFriendships || '当朋友时';
      document.querySelectorAll('[data-section="section-intro"]').forEach(a => a.textContent = navIntro);
      document.querySelectorAll('[data-section="section-romantic"]').forEach(a => a.textContent = navRomantic);
      document.querySelectorAll('[data-section="section-friends"]').forEach(a => a.textContent = navFriends);
    }

    function showScreen(name) {
      Object.entries(screens).forEach(([key, el]) => {
        el.classList.toggle('active', key === name);
      });
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function shuffle(array) {
      const arr = [...array];
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
      return arr;
    }

    function getVisibleQuestions() {
      const visible = [...app.shuffledQuestions];
      const gateIndex = visible.findIndex(q => q.id === 'drink_gate_q1');
      if (gateIndex !== -1 && app.answers['drink_gate_q1'] === 3) {
        visible.splice(gateIndex + 1, 0, specialQuestions[1]);
      }
      return visible;
    }

    function getQuestionMetaLabel(q) {
      if (q.special) return uiText.question.specialMeta;
      return app.previewMode ? dimensionMeta[q.dim].name : uiText.question.hiddenMeta;
    }

    function bindBrowseClicks(container) {
      container.querySelectorAll('[data-browse-code]').forEach((card) => {
        card.onclick = () => openTypeDetail(card.dataset.browseCode);
      });
    }

    const IMAGE_ASSET_VERSION = '20260410-band-fix-1';

    function getTypeImageSrc(code) {
      const src = TYPE_IMAGES[code];
      return src ? `${src}?v=${IMAGE_ASSET_VERSION}` : '';
    }

    function renderBandType(code) {
      const type = TYPE_LIBRARY[code];
      const imgSrc = getTypeImageSrc(code);
      const imgHtml = imgSrc
        ? `<img src="${imgSrc}" alt="${type.code}" onerror="this.style.display='none'" />`
        : '';
      return `
        <article class="band-type" data-browse-code="${type.code}">
          <div class="band-figure">${imgHtml}</div>
          <div class="band-name">${type.cn}</div>
          <div class="band-code">${type.code}</div>
          <div class="band-intro">${type.intro}</div>
        </article>
      `;
    }

    function renderEasterType(code) {
      const type = TYPE_LIBRARY[code];
      const imgSrc = getTypeImageSrc(code);
      const imgHtml = imgSrc
        ? `<img src="${imgSrc}" alt="${type.code}" onerror="this.style.display='none'" />`
        : '';
      return `
        <article class="catalog-easter-card" data-browse-code="${type.code}">
          <div class="catalog-easter-figure">${imgHtml}</div>
          <div class="catalog-easter-copy">
            <span class="catalog-easter-code">${type.code}</span>
            <h4>${type.cn}</h4>
            <p>${type.intro}</p>
          </div>
        </article>
      `;
    }

    function renderBrowseCatalog() {
      browseMainGrid.innerHTML = BROWSE_GROUPS.map(group => `
        <section class="catalog-band catalog-band--${group.theme}">
          <div class="catalog-band-watermark">${group.watermark}</div>
          <div class="catalog-band-head">
            <div class="catalog-band-kicker">${group.kicker}</div>
            <h3>${group.title}</h3>
            <p>${group.desc}</p>
          </div>
          <div class="catalog-band-grid">
            ${group.codes.map(renderBandType).join('')}
          </div>
        </section>
      `).join('');

      browseEasterGrid.innerHTML = EASTER_EGG_TYPES.map(renderEasterType).join('');
      bindBrowseClicks(browseMainGrid);
      bindBrowseClicks(browseEasterGrid);
    }

    function renderQuestions() {
      const visibleQuestions = getVisibleQuestions();
      questionList.innerHTML = '';
      visibleQuestions.forEach((q, index) => {
        const card = document.createElement('article');
        card.className = 'question';
        card.innerHTML = `
          <div class="question-meta">
            <div class="badge">${formatText(uiText.question.numberTemplate, { index: index + 1 })}</div>
            <div>${getQuestionMetaLabel(q)}</div>
          </div>
          <div class="question-title">${q.text}</div>
          <div class="options">
            ${q.options.map((opt, i) => {
              const code = ['A', 'B', 'C', 'D'][i] || String(i + 1);
              const checked = app.answers[q.id] === opt.value ? 'checked' : '';
              return `
                <label class="option">
                  <input type="radio" name="${q.id}" value="${opt.value}" ${checked} />
                  <div class="option-code">${code}</div>
                  <div>${opt.label}</div>
                </label>
              `;
            }).join('')}
          </div>
        `;
        questionList.appendChild(card);
      });

      questionList.querySelectorAll('input[type="radio"]').forEach(input => {
        input.addEventListener('change', (e) => {
          const { name, value } = e.target;
          app.answers[name] = Number(value);

          if (name === 'drink_gate_q1') {
            if (Number(value) !== 3) {
              delete app.answers['drink_gate_q2'];
            }
            renderQuestions();
            return;
          }

          updateProgress();
        });
      });

      updateProgress();
    }

    function updateProgress() {
      const visibleQuestions = getVisibleQuestions();
      const total = visibleQuestions.length;
      const done = visibleQuestions.filter(q => app.answers[q.id] !== undefined).length;
      const percent = total ? (done / total) * 100 : 0;
      progressBar.style.width = `${percent}%`;
      progressText.textContent = formatText(uiText.templates.progress, { done, total });
      const complete = done === total && total > 0;
      submitBtn.disabled = !complete;
      testHint.textContent = complete
        ? uiText.progress.completeHint
        : uiText.progress.incompleteHint;
    }

    function sumToLevel(score) {
      if (score <= 3) return 'L';
      if (score === 4) return 'M';
      return 'H';
    }

    function levelNum(level) {
      return { L: 1, M: 2, H: 3 }[level];
    }

    function parsePattern(pattern) {
      return pattern.replace(/-/g, '').split('');
    }

    const TYPE_PATTERN_MAP = Object.fromEntries(
      NORMAL_TYPES.map(type => [type.code, parsePattern(type.pattern)])
    );

    function getCompatibilityAffinity(kind, diff) {
      if (kind === 'same') {
        if (diff === 0) return 1;
        if (diff === 1) return 0.55;
        return -0.45;
      }
      if (kind === 'adjacent') {
        if (diff === 1) return 1;
        if (diff === 0) return 0.72;
        return 0.1;
      }
      return 0;
    }

    function computeCompatibilityDetails(baseCode, candidateCode, mode) {
      const baseVector = TYPE_PATTERN_MAP[baseCode];
      const candidateVector = TYPE_PATTERN_MAP[candidateCode];
      const rule = COMPATIBILITY_RULES[mode];
      if (!baseVector || !candidateVector || !rule) return null;

      let total = 0;
      let max = 0;
      let distance = 0;
      const contributions = [];

      dimensionOrder.forEach((dim, index) => {
        const [kind, weight] = rule.weights[dim];
        const diff = Math.abs(levelNum(baseVector[index]) - levelNum(candidateVector[index]));
        const affinity = getCompatibilityAffinity(kind, diff);
        const weighted = affinity * weight;
        total += weighted;
        max += weight;
        distance += diff;
        contributions.push({ dim, weighted, diff });
      });

      contributions.sort((a, b) => b.weighted - a.weighted || a.diff - b.diff || a.dim.localeCompare(b.dim));
      return {
        score: Math.max(0, Math.min(100, Math.round((total / max) * 100))),
        distance,
        topReasons: contributions
          .filter(item => item.weighted > 0)
          .slice(0, 3)
          .map(item => rule.reasonLabels[item.dim])
      };
    }

    function computeBestRelationshipMatch(baseCode, mode) {
      const special = COMPATIBILITY_SPECIAL_MATCHES[mode]?.[baseCode];
      if (special) return { ...special, special: true };
      if (!TYPE_PATTERN_MAP[baseCode]) return null;

      const ranked = NORMAL_TYPE_CODES
        .filter(code => code !== baseCode)
        .map(code => ({ code, ...computeCompatibilityDetails(baseCode, code, mode) }))
        .filter(Boolean)
        .sort((a, b) => b.score - a.score || a.distance - b.distance || a.code.localeCompare(b.code));

      return ranked[0] || null;
    }

    function getRelationshipCopy(mode, baseCode, matchCode) {
      const pairKey = `${mode}|${baseCode}|${matchCode}`;
      const copy = COMPATIBILITY_TEXT?.[pairKey];
      if (!copy) return null;
      const summary = isPlaceholder(copy.summary) ? '' : copy.summary;
      const highlight = isPlaceholder(copy.highlight) ? '' : copy.highlight;
      if (!summary && !highlight) return null;
      return { summary, highlight };
    }

    function getCompatibilityFallbackCopy(mode, baseType, matchType) {
      if (mode === 'friendship') {
        return {
          summary: `${baseType.cn}和${matchType.cn}凑朋友局，基本属于一边犯轴另一边也看得懂。能一起整活，也能一起把场面搞得有点难收。`,
          highlight: '这对能玩到一块，但也很容易把好日子过得鸡飞狗跳。'
        };
      }
      return {
        summary: `${baseType.cn}和${matchType.cn}谈恋爱，不是完全不搭，是真容易一边上头一边互相折腾。甜的时候很甜，翻车的时候也不会给彼此留脸。`,
        highlight: '这对谈起来有火花，炸起来也够把人炸清醒。'
      };
    }

    function renderCompatibilityBox(type) {
      const compatibilityBox = document.getElementById('compatibilityBox');
      const compatibilityUI = uiText.compatibility || {};
      const cards = ['friendship', 'romantic'].map((mode) => {
        const match = computeBestRelationshipMatch(type.code, mode);
        if (!match) return '';
        const matchType = TYPE_LIBRARY[match.code];
        if (!matchType) return '';
        const modeTitle = mode === 'friendship'
          ? (compatibilityUI.friendshipTitle || '朋友最佳匹配')
          : (compatibilityUI.romanticTitle || '恋爱最佳匹配');
        const badge = mode === 'friendship'
          ? (compatibilityUI.friendshipBadge || '最适合一起鬼混')
          : (compatibilityUI.romanticBadge || '最容易谈出事');
        const copy = getRelationshipCopy(mode, type.code, match.code) || getCompatibilityFallbackCopy(mode, type, matchType);
        const reasonTitle = compatibilityUI.reasonsTitle || '能凑一块的原因';
        const scoreLabel = compatibilityUI.scoreLabel || '适配度';
        const reasons = (match.topReasons || []).slice(0, 3);
        const imageSrc = getTypeImageSrc(match.code);
        const figureHtml = imageSrc ? `<img src="${imageSrc}" alt="${match.code}" onerror="this.style.display='none'" />` : '';
        return `
          <article class="compat-card">
            <div class="compat-card-head">
              <div>
                <div class="compat-kicker">${modeTitle}</div>
                <h4>${badge}</h4>
                <div class="compat-card-sub">${formatText(uiText.templates.typeName, { code: match.code, cn: matchType.cn })}</div>
              </div>
              <div class="compat-score">
                <div class="compat-score-label">${scoreLabel}</div>
                <div class="compat-score-value">${match.score}</div>
              </div>
            </div>
            <div class="compat-match">
              <div class="compat-match-figure">${figureHtml}</div>
              <div>
                <div class="compat-match-code">${match.code}</div>
                <div class="compat-match-name">${matchType.cn}</div>
                <div class="compat-match-intro">${matchType.intro}</div>
              </div>
            </div>
            <div class="compat-copy">${copy.summary || ''}</div>
            ${copy.highlight ? `<div class="compat-callout">${copy.highlight}</div>` : ''}
            ${reasons.length ? `
              <div>
                <div class="compat-reasons-title">${reasonTitle}</div>
                <div class="compat-reasons">
                  ${reasons.map(reason => `<span class="compat-reason">${reason}</span>`).join('')}
                </div>
              </div>
            ` : ''}
          </article>
        `;
      }).filter(Boolean).join('');

      if (!cards) {
        compatibilityBox.classList.add('is-hidden');
        compatibilityBox.innerHTML = '';
        return;
      }

      compatibilityBox.classList.remove('is-hidden');
      compatibilityBox.innerHTML = `
        <div class="compatibility-head">
          <h3>${compatibilityUI.sectionTitle || '最佳匹配'}</h3>
          <p>${compatibilityUI.sectionSub || '朋友局、恋爱局各有各的翻车法，别拿一把尺子从头量到尾。'}</p>
        </div>
        <div class="compatibility-grid">${cards}</div>
      `;
    }

    function getDrunkTriggered() {
      return app.answers[DRUNK_TRIGGER_QUESTION_ID] === 2;
    }

    function computeResult() {
      const rawScores = {};
      const levels = {};
      Object.keys(dimensionMeta).forEach(dim => { rawScores[dim] = 0; });

      questions.forEach(q => {
        rawScores[q.dim] += Number(app.answers[q.id] || 0);
      });

      Object.entries(rawScores).forEach(([dim, score]) => {
        levels[dim] = sumToLevel(score);
      });

      const userVector = dimensionOrder.map(dim => levelNum(levels[dim]));
      const ranked = NORMAL_TYPES.map(type => {
        const vector = parsePattern(type.pattern).map(levelNum);
        let distance = 0;
        let exact = 0;
        for (let i = 0; i < vector.length; i++) {
          const diff = Math.abs(userVector[i] - vector[i]);
          distance += diff;
          if (diff === 0) exact += 1;
        }
        const similarity = Math.max(0, Math.round((1 - distance / 30) * 100));
        return { ...type, ...TYPE_LIBRARY[type.code], distance, exact, similarity };
      }).sort((a, b) => {
        if (a.distance !== b.distance) return a.distance - b.distance;
        if (b.exact !== a.exact) return b.exact - a.exact;
        return b.similarity - a.similarity;
      });

      const bestNormal = ranked[0];
      const drunkTriggered = getDrunkTriggered();

      let finalType;
      let modeKicker = uiText.resultStates.normal.modeKicker;
      let badge = formatText(uiText.templates.badgeNormal, {
        similarity: bestNormal.similarity,
        exact: bestNormal.exact
      });
      let sub = uiText.resultStates.normal.sub;
      let special = false;
      let secondaryType = null;

      if (drunkTriggered) {
        finalType = TYPE_LIBRARY.DRUNK;
        secondaryType = bestNormal;
        modeKicker = uiText.resultStates.drunk.modeKicker;
        badge = uiText.resultStates.drunk.badge;
        sub = uiText.resultStates.drunk.sub;
        special = true;
      } else if (bestNormal.similarity < 60) {
        finalType = TYPE_LIBRARY.HHHH;
        modeKicker = uiText.resultStates.fallback.modeKicker;
        badge = formatText(uiText.templates.badgeFallback, { similarity: bestNormal.similarity });
        sub = uiText.resultStates.fallback.sub;
        special = true;
      } else {
        finalType = bestNormal;
      }

      return {
        rawScores,
        levels,
        ranked,
        bestNormal,
        finalType,
        modeKicker,
        badge,
        sub,
        special,
        secondaryType
      };
    }

    function renderDimList(result) {
      const dimList = document.getElementById('dimList');
      dimList.innerHTML = dimensionOrder.map(dim => {
        const level = result.levels[dim];
        const explanation = DIM_EXPLANATIONS[dim][level];
        return `
          <div class="dim-item">
            <div class="dim-item-top">
              <div class="dim-item-name">${dimensionMeta[dim].name}</div>
              <div class="dim-item-score">${formatText(uiText.templates.dimScore, { level, score: result.rawScores[dim] })}</div>
            </div>
            <p>${explanation}</p>
          </div>
        `;
      }).join('');
    }

    function setResultMode(mode) {
      app.resultViewMode = mode;
      restartBtn.textContent = mode === 'browse'
        ? uiText.buttons.start
        : uiText.buttons.restart;
      resultBrowseBtn.textContent = mode === 'browse'
        ? uiText.buttons.backBrowse
        : uiText.buttons.browseAll;
    }

    function isPlaceholder(text) {
      return !text || String(text).trim().startsWith('__GEMINI__');
    }

    function renderRelationSection(container, data, displayTitle) {
      const wrapper = container.parentElement;
      if (!data || !data.title || isPlaceholder(data.lead)) {
        wrapper.classList.add('is-hidden');
        container.innerHTML = '';
        return false;
      }
      wrapper.classList.remove('is-hidden');
      container.innerHTML = `
        <h2>${displayTitle || data.title}</h2>
        <p class="relation-lead">${data.lead}</p>
        ${data.callout && !isPlaceholder(data.callout) ? `<div class="relation-callout">${data.callout}</div>` : ''}
        ${(data.sections || []).filter(s => !isPlaceholder(s.body)).map(s => `
          <div class="relation-sub">
            <h3>${s.heading}</h3>
            <p>${s.body}</p>
          </div>
        `).join('')}
      `;
      return true;
    }

    function updateDetailNav(hasRomantic, hasFriends) {
      const sectionCount = 1 + (hasRomantic ? 1 : 0) + (hasFriends ? 1 : 0);
      document.getElementById('detailSidebar').classList.toggle('is-hidden', sectionCount <= 1);
      const pills = document.getElementById('detailPills');
      pills.classList.toggle('is-hidden', sectionCount <= 1);

      document.querySelectorAll('[data-section="section-romantic"]').forEach(el => {
        el.style.display = hasRomantic ? '' : 'none';
      });
      document.querySelectorAll('[data-section="section-friends"]').forEach(el => {
        el.style.display = hasFriends ? '' : 'none';
      });

      document.querySelectorAll('.detail-nav a, .detail-pills a').forEach(a => {
        a.classList.remove('active');
      });
      document.querySelectorAll('[data-section="section-intro"]').forEach(a => {
        a.classList.add('active');
      });
    }

    let detailObserver = null;
    function setupDetailNavObserver() {
      if (detailObserver) detailObserver.disconnect();

      const sectionIds = ['section-intro', 'section-romantic', 'section-friends'];
      const allNavLinks = document.querySelectorAll('.detail-nav a, .detail-pills a');

      detailObserver = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const targetId = entry.target.id;
            allNavLinks.forEach(link => {
              link.classList.toggle('active', link.dataset.section === targetId);
            });
            break;
          }
        }
      }, { rootMargin: '-10% 0px -70% 0px' });

      sectionIds.forEach(id => {
        const el = document.getElementById(id);
        if (el && !el.classList.contains('is-hidden')) {
          detailObserver.observe(el);
        }
      });

      allNavLinks.forEach(link => {
        link.onclick = (e) => {
          e.preventDefault();
          const targetId = link.dataset.section;
          const target = document.getElementById(targetId);
          if (target) target.scrollIntoView({ behavior: 'smooth' });
        };
      });
    }

    function renderTypeDetail({ type, modeKicker, badge, sub, note, showMatch, showDims, result, mode }) {
      setResultMode(mode);

      resultModeKicker.textContent = modeKicker;
      resultTypeName.textContent = formatText(uiText.templates.typeName, { code: type.code, cn: type.cn });
      matchBadge.textContent = badge || '';
      resultTypeSub.textContent = sub;
      resultDesc.textContent = type.desc;
      posterCaption.textContent = type.intro;
      funNote.textContent = note;
      matchBadge.classList.toggle('is-hidden', !showMatch);
      dimBox.classList.toggle('is-hidden', !showDims);

      const posterBox = document.getElementById('posterBox');
      const imageSrc = getTypeImageSrc(type.code);
      if (imageSrc) {
        posterImage.src = imageSrc;
        posterImage.alt = formatText(uiText.templates.typeName, { code: type.code, cn: type.cn });
        posterBox.classList.remove('no-image');
      } else {
        posterImage.removeAttribute('src');
        posterImage.alt = uiText.result.posterAlt;
        posterBox.classList.add('no-image');
      }

      if (showDims && result) {
        renderDimList(result);
      } else {
        document.getElementById('dimList').innerHTML = '';
      }

      renderCompatibilityBox(type);

      const detailUI = uiText.detail || {};
      const hasRomantic = renderRelationSection(
        document.getElementById('romanticSection'),
        type.romanticRelationships,
        detailUI.navRomantic || '谈恋爱时'
      );
      const hasFriends = renderRelationSection(
        document.getElementById('friendsSection'),
        type.friendships,
        detailUI.navFriendships || '当朋友时'
      );
      updateDetailNav(hasRomantic, hasFriends);

      showScreen('result');
      requestAnimationFrame(() => setupDetailNavObserver());
    }

    function renderResult(source = 'test') {
      const result = computeResult();
      const type = result.finalType;
      const isRandom = source === 'random';

      const modeKicker = isRandom
        ? formatText(uiText.resultStates.random.modeKickerTemplate, { mode: result.modeKicker })
        : result.modeKicker;
      const sub = isRandom
        ? formatText(uiText.resultStates.random.subTemplate, { base: result.sub })
        : result.sub;
      const note = isRandom
        ? uiText.notes.random
        : (result.special ? uiText.notes.special : uiText.notes.normal);

      renderTypeDetail({
        type,
        modeKicker,
        badge: result.badge,
        sub,
        note,
        showMatch: true,
        showDims: true,
        result,
        mode: isRandom ? 'random' : 'test'
      });
    }

    function openTypeDetail(code) {
      const type = TYPE_LIBRARY[code];
      if (!type) return;
      renderTypeDetail({
        type,
        modeKicker: uiText.browse.detailKicker,
        badge: '',
        sub: uiText.browse.detailSub,
        note: uiText.browse.detailNote,
        showMatch: false,
        showDims: false,
        result: null,
        mode: 'browse'
      });
    }

    function getRandomOptionValue(question) {
      const options = question.options || [];
      const picked = options[Math.floor(Math.random() * options.length)];
      return picked ? picked.value : undefined;
    }

    function generateRandomAnswers() {
      const answers = {};
      questions.forEach((question) => {
        answers[question.id] = getRandomOptionValue(question);
      });

      const gateQuestion = specialQuestions[0];
      answers[gateQuestion.id] = getRandomOptionValue(gateQuestion);

      if (answers[gateQuestion.id] === 3) {
        answers[specialQuestions[1].id] = getRandomOptionValue(specialQuestions[1]);
      }

      return answers;
    }

    function startRandomResult() {
      app.previewMode = false;
      app.shuffledQuestions = [];
      app.answers = generateRandomAnswers();
      renderResult('random');
    }

    function startTest(preview = false) {
      app.previewMode = preview;
      app.answers = {};
      const shuffledRegular = shuffle(questions);
      const insertIndex = Math.floor(Math.random() * shuffledRegular.length) + 1;
      app.shuffledQuestions = [
        ...shuffledRegular.slice(0, insertIndex),
        specialQuestions[0],
        ...shuffledRegular.slice(insertIndex)
      ];
      renderQuestions();
      showScreen('test');
    }

    applyStaticTexts();
    renderBrowseCatalog();
    document.getElementById('startBtn').addEventListener('click', () => startTest(false));
    document.getElementById('browseBtn').addEventListener('click', () => {
      renderBrowseCatalog();
      showScreen('browse');
    });
    document.getElementById('randomBtn').addEventListener('click', startRandomResult);
    document.getElementById('browseBackBtn').addEventListener('click', () => showScreen('intro'));
    document.getElementById('browseStartBtn').addEventListener('click', () => startTest(false));
    document.getElementById('backIntroBtn').addEventListener('click', () => showScreen('intro'));
    document.getElementById('submitBtn').addEventListener('click', () => renderResult('test'));
    document.getElementById('restartBtn').addEventListener('click', () => startTest(false));
    document.getElementById('resultBrowseBtn').addEventListener('click', () => {
      renderBrowseCatalog();
      showScreen('browse');
    });
    document.getElementById('toTopBtn').addEventListener('click', () => showScreen('intro'));
  