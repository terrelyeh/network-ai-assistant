# EnGenius Cloud Design Tokens

> **這份文件不是新寫的 design system** — 是「對齊既有 EnGenius Cloud GUI 的快照」。
> Dashboard Builder widget 的視覺實作直接 reuse 這些 token，不要另寫一套。
>
> **來源**：直接從 https://www.engenius.ai/cloud/ 抓 CSS / 推斷常見 dashboard 慣例
> Last updated: 2026-05-06

---

## 1. Color Tokens

### Primary Brand

| Token | Hex | 用途 |
|---|---|---|
| `--brand-primary` | `#03A9F4` | 主 accent · CTA 連結 · 圖表主線 |
| `--brand-secondary` | `#2F5BE7` | 次要藍 · 強調區塊 |
| `--brand-deep` | `#291734` | 深色背景區塊（hero / footer） |

### Semantic

| Token | Hex | 用途 |
|---|---|---|
| `--success` | `#10B981` | 健康 · 通過 · 良好 |
| `--warning` | `#F59E0B` | 注意 · 警示（非緊急） |
| `--danger` | `#EA3D56` | 嚴重 · 錯誤 · 紅燈 |
| `--info` | `#03A9F4` | 提示 · 中性訊息（同 brand-primary） |
| `--cta-orange` | `#FFA200` | CTA 強調（用於促購 / 訂閱按鈕） |

### Surface (Backgrounds)

| Token | Hex | 用途 |
|---|---|---|
| `--bg-primary` | `#FFFFFF` | 主底色 · 卡片底 |
| `--bg-section` | `#ECF2FF` | 區塊底色（淺藍灰） |
| `--bg-subtle` | `#F8FAFC` | 表格條紋 · disabled state |
| `--bg-hover` | `#EBF4FE` | 互動 hover 底色 |

### Text

| Token | Hex | 用途 |
|---|---|---|
| `--text-heading` | `#32373C` | 標題（H1-H4） |
| `--text-body` | `#4A5568` | 主要內文 |
| `--text-muted` | `#7D7D7D` | 次要說明 · 註解 |
| `--text-dim` | `#A0AEC0` | 最弱層級 · placeholder |
| `--text-on-dark` | `#FFFFFF` | 深色背景上的文字 |

### Border / Divider

| Token | Hex | 用途 |
|---|---|---|
| `--border-default` | `#CECECE` | 一般邊框 |
| `--border-subtle` | `#E2E8F0` | 表格 / 卡片 hairline |
| `--border-strong` | `#94A3B8` | input focus · 強化 |

---

## 2. Chart Palette（資料視覺化）

按使用順序 — categorical chart 取前 N 個。

| 順序 | Token | Hex | 視覺 |
|---|---|---|---|
| 1 | `--chart-1` | `#03A9F4` | Sky blue · brand 主色 |
| 2 | `--chart-2` | `#2F5BE7` | Deep blue |
| 3 | `--chart-3` | `#FFA200` | Orange |
| 4 | `--chart-4` | `#10B981` | Green |
| 5 | `--chart-5` | `#A78BFA` | Purple |
| 6 | `--chart-6` | `#EA3D56` | Red |
| 7 | `--chart-7` | `#06B6D4` | Cyan |
| 8 | `--chart-8` | `#F59E0B` | Amber |

**規則**：
- categorical chart **不超過 5 條線** → 用前 5 色
- comparison（本週 vs 上週）用同色不同明度，不要兩個對比色
- error / 嚴重狀態固定用 `--danger`（不要用 `--chart-6`）
- 健康狀態固定用 `--success` / `--warning` / `--danger`，不要 chart palette 染色

**Sequential gradient（heatmap / density map）**：
```
#ECF2FF → #B8D4FB → #69A8F0 → #03A9F4 → #2F5BE7
```

---

## 3. Typography

### Font Family

```css
--font-sans: 'Inter', 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'JetBrains Mono', 'Roboto Mono', Consolas, monospace;
```

> EnGenius Cloud GUI 觀察到主要用 sans-serif，建議跟我們提案站一致用 Inter + Noto Sans TC。

### Type Scale

| Token | Size | Weight | Line-height | 用途 |
|---|---|---|---|---|
| `--text-display` | 48px | 900 | 1.1 | Hero / 大標 |
| `--text-h1` | 32px | 800 | 1.2 | 頁面主標 |
| `--text-h2` | 24px | 700 | 1.3 | 區塊標題 |
| `--text-h3` | 18px | 700 | 1.4 | 卡片標題 |
| `--text-body-lg` | 17px | 400 | 1.65 | Lead / 重要描述 |
| `--text-body` | 15px | 400 | 1.6 | 一般內文 |
| `--text-body-sm` | 13px | 400 | 1.55 | 次要內文 / 表格 cell |
| `--text-caption` | 12px | 600 | 1.5 | 標籤 / 註腳 |
| `--text-mono` | 13px | 500 | 1.5 | 程式碼 / KPI 數字 |

### Weight Scale

| Token | Value | 用途 |
|---|---|---|
| `--weight-regular` | 400 | 一般內文 |
| `--weight-medium` | 500 | 次要強調 / mono 數字 |
| `--weight-semibold` | 600 | 標籤 / button 文字 |
| `--weight-bold` | 700 | 標題 |
| `--weight-extrabold` | 800-900 | 大標 / display |

### Numeric

KPI / 表格數字統一用 `font-feature-settings: 'tnum'` 或 `font-variant-numeric: tabular-nums` — 確保等寬數字對齊。

---

## 4. Spacing Scale

跟 Tailwind 對齊（4px base）：

| Token | Pixels | 用途 |
|---|---|---|
| `--space-1` | 4px | hairline / icon offset |
| `--space-2` | 8px | small gap |
| `--space-3` | 12px | inline gap |
| `--space-4` | 16px | card padding inner |
| `--space-5` | 20px | between elements |
| `--space-6` | 24px | card padding default |
| `--space-8` | 32px | section padding |
| `--space-10` | 40px | between sections |
| `--space-12` | 48px | between major sections |
| `--space-16` | 64px | hero padding |

---

## 5. Border Radius

| Token | Value | 用途 |
|---|---|---|
| `--radius-sm` | 4px | input / small badge |
| `--radius-md` | 6px | button |
| `--radius-lg` | 8px | code block / small card |
| `--radius-xl` | 12px | card default |
| `--radius-2xl` | 16px | hero card / modal |
| `--radius-full` | 9999px | pill / avatar |

---

## 6. Shadows

| Token | Value | 用途 |
|---|---|---|
| `--shadow-sm` | `0 1px 3px rgba(15,30,60,0.06)` | 卡片 hairline |
| `--shadow-md` | `0 4px 12px rgba(15,30,60,0.10)` | 卡片 hover |
| `--shadow-lg` | `0 12px 30px rgba(15,30,60,0.12)` | modal / dropdown |
| `--shadow-glow-primary` | `0 0 0 3px rgba(3,169,244,0.20)` | input focus ring |

---

## 7. Z-index Scale

| Token | Value | 用途 |
|---|---|---|
| `--z-base` | 0 | 基準 |
| `--z-sticky` | 10 | sticky header / TOC |
| `--z-dropdown` | 50 | dropdown / popover |
| `--z-modal` | 100 | modal / dialog |
| `--z-toast` | 1000 | toast notification |

---

## 8. Animation / Transition

| Token | Value | 用途 |
|---|---|---|
| `--duration-fast` | 150ms | hover / button press |
| `--duration-normal` | 250ms | panel slide |
| `--duration-slow` | 400ms | modal / page transition |
| `--ease-default` | `cubic-bezier(0.4, 0, 0.2, 1)` | 預設 easing |

---

## 9. 給 RD 的快速使用建議

### CSS Variable 命名
直接用上面的 `--xxx` 名字進 `:root`，跨 widget 統一引用：
```css
.kpi-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  font-size: var(--text-body);
  color: var(--text-body);
}
.kpi-card .value {
  font-size: var(--text-display);
  font-weight: var(--weight-extrabold);
  color: var(--text-heading);
  font-variant-numeric: tabular-nums;
}
```

### Tailwind 對應
如果 stack 用 Tailwind，`tailwind.config.js` 直接 extend：
```js
theme: {
  extend: {
    colors: {
      brand: { primary: '#03A9F4', secondary: '#2F5BE7' },
      // ...
    },
    fontFamily: {
      sans: ['Inter', 'Noto Sans TC', 'sans-serif'],
    }
  }
}
```

---

## 10. 還沒解決的設計疑點

- [ ] Dark mode 要不要支援？v1 建議先不做（既有 EnGenius Cloud 也是 light only）
- [ ] 字體 license：Inter 是 OFL 開源，Noto Sans TC 是 SIL 開源，可商用
- [ ] 圖表 library 的內建色被覆寫到什麼程度（Recharts 預設色完全不要用？）
- [ ] 已經有 EnGenius 內部的 design system 嗎？這份是 reverse-engineered，正式版要跟 design 部門對齊
