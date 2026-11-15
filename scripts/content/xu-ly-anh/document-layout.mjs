import katex from 'katex';

export const escapeHtml=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const canonical=value=>Array.isArray(value)?value.map(canonical):value!==null&&typeof value==='object'?Object.fromEntries(Object.keys(value).sort().map(k=>[k,canonical(value[k])])):value;
const e=escapeHtml;
const math=tex=>katex.renderToString(tex,{displayMode:true,throwOnError:true,trust:false,output:'html'});
const text=value=>e(value).replace(/\b(I_DCT|I_Q|e_rms|DC_truoc|e_old|e_new)\b/g,word=>{const [base,...sub]=word.split('_');return `${base}<sub>${sub.join('_')}</sub>`;});

function table(block){
  let headers=block.headers,rows=block.rows;
  let legend='';
  if(headers[0]==='cây con trái'&&headers[2]==='cây con phải'){
    const names=new Map();
    const key=value=>String(value).startsWith('(')?String(value).replace(/\s/g,''):`'${value}'`;
    rows=rows.map((r,i)=>{
      const left=key(r[0]),right=key(r[2]),node='N'+(i+1);
      const converted=[names.get(left)??r[0],r[1],names.get(right)??r[2],r[3],node,r[4]];
      names.set(`(${left},${right})`,node);return converted;
    });
    headers=['con trái','n trái','con phải','n phải','nút mới','n mới'];
    legend='<p class="table-note">N₁, N₂, … là các nút ghép lần lượt; hai con của mỗi nút được ghi trên cùng dòng.</p>';
  }
  // Histogram tables use the horizontal layout of the supplied answer key.
  const transpose=rows.length<=10&&headers.length<=4&&/^(g|s)$/.test(headers[0]);
  if(transpose){rows=headers.map((h,i)=>[h,...block.rows.map(row=>row[i])]);headers=null;}
  return `<figure class="data-table">${block.caption?`<figcaption>${text(block.caption)}</figcaption>`:''}${legend}<table>${headers?`<thead><tr>${headers.map(h=>`<th>${text(h)}</th>`).join('')}</tr></thead>`:''}<tbody>${rows.map(row=>`<tr>${row.map((v,i)=>`<${transpose&&i===0?'th':'td'}>${text(v)}</${transpose&&i===0?'th':'td'}>`).join('')}</tr>`).join('')}</tbody></table></figure>`;
}
function matrix(block){return `<figure class="matrix-figure"><div class="matrix-brackets"><table>${block.rows.map(row=>`<tr>${row.map(v=>`<td>${text(v)}</td>`).join('')}</tr>`).join('')}</table></div>${block.caption?`<figcaption>${text(block.caption)}</figcaption>`:''}</figure>`;}
function blockHtml(block){
  if(block.type==='table')return table(block);
  if(block.type==='matrix')return matrix(block);
  if(block.type==='formula')return `<div class="equation" data-tex="${e(block.tex)}">${math(block.tex)}</div>`;
  if(block.type==='code')return `<pre>${e(block.code)}</pre>`;
  throw new Error('Unexpected exercise block: '+block.type);
}
function blocksHtml(blocks=[]){
  let html='';
  for(let i=0;i<blocks.length;i++){
    if(blocks[i].type==='matrix'&&blocks[i+1]?.type==='matrix'){
      html+=`<div class="matrix-pair">${matrix(blocks[i])}${matrix(blocks[++i])}</div>`;
    }else html+=blockHtml(blocks[i]);
  }
  return html;
}

export function exerciseHtml(item,sources,images){
  const area=item.area==='bank'?`giải ngân hàng · ${item.points} điểm`:`giải bài cô Uyên · Chương ${item.chapter}`;
  const refs=item.references.map(r=>`${sources.find(s=>s.id===r.sourceId)?.title??r.sourceId}, trang PDF ${r.pdfPage}`).filter((r,i,a)=>a.indexOf(r)===i);
  return `<header class="item-header"><p class="area">XỬ LÝ ẢNH · ${e(area)}</p><h1>Bài ${e(item.code)}. ${e(item.title)}</h1></header>
    <section class="problem"><h2>Đề bài</h2>${images.map((src,i)=>`<figure class="prompt-figure"><img src="${src}" alt="Đề gốc bài ${e(item.code)}, phần ${i+1}"></figure>`).join('')}</section>
    <section class="answer-start"><h2>BÀI GIẢI · Bài ${e(item.code)}</h2><p class="answer-cue"><strong>Cần nhớ:</strong> ${item.keywords.map(e).join(' · ')}</p>
    ${item.note?`<aside class="correction"><strong>Lưu ý dữ kiện / quy ước:</strong> ${text(item.note)}</aside>`:''}
    ${item.steps.map((s,i)=>`<section class="answer-step" data-step="${i}"><h3>Bước ${i+1}. ${e(s.lead)}</h3>
      ${s.formula?`<p class="label">Áp dụng công thức:</p><div class="equation" data-tex="${e(s.formula)}">${math(s.formula)}</div>`:''}
      ${s.substitution?`<p class="substitution"><strong>Thay số / thực hiện:</strong> ${text(s.substitution)}</p>`:''}
      ${s.text?`<p>${text(s.text)}</p>`:''}
      ${blocksHtml(s.blocks)}
      ${s.result?`<p class="result"><strong>Kết luận:</strong> ${text(s.result)}</p>`:''}</section>`).join('')}
    <section class="references"><h3>Nguồn đối chiếu</h3><ul>${refs.map(r=>`<li>${e(r)}</li>`).join('')}</ul></section></section>`;
}

export const printCss=`
@page{size:A4;margin:17mm 16mm 18mm}
*{box-sizing:border-box}html{background:white;color:#111}body{margin:0;font-family:'Times New Roman','Liberation Serif',serif;font-size:13.5pt;line-height:1.42}
h1{font-size:19pt;line-height:1.3;margin:6pt 0 14pt}h2{font-size:17pt;margin:12pt 0 10pt}h3{font-size:14pt;line-height:1.4;margin:16pt 0 7pt;break-after:avoid-page}p{margin:7pt 0;orphans:3;widows:3}.area{font-family:Arial,sans-serif;font-size:10pt;letter-spacing:.25pt;color:#3c5147}.item-header{border-bottom:1pt solid #555;padding-bottom:8pt}.prompt-figure{margin:8pt 0;break-inside:avoid}.prompt-figure img{display:block;max-width:100%;max-height:225mm;object-fit:contain;margin:0 auto}.answer-start{break-before:page}.answer-start>h2{text-align:center;margin-top:0}.answer-cue{font-style:italic;margin-bottom:12pt}.correction{padding:9pt 12pt;border-left:2pt solid #555;background:#f4f4f4;font-size:12pt;margin:10pt 0;break-inside:avoid}.label{margin:6pt 0 0;font-style:italic;break-after:avoid}.equation{text-align:center;font-size:13pt;margin:5pt 0 10pt;break-inside:avoid}.katex-display{margin:.4em 0}.katex{font-size:1.05em}.substitution{margin:8pt 0}.result{font-weight:normal;margin:10pt 0}.result strong{border-bottom:1px solid #333}figure{margin:10pt 0 14pt;max-width:100%}figcaption{font-style:italic;text-align:center;font-size:12pt;margin:5pt 0}.matrix-figure{display:flex;align-items:center;flex-direction:column;break-inside:avoid}.matrix-brackets{display:inline-block;position:relative;padding:3pt 8pt;border-left:1.3pt solid #111;border-right:1.3pt solid #111}.matrix-brackets:before,.matrix-brackets:after{content:'';position:absolute;inset:0;border-top:1.3pt solid #111;border-bottom:1.3pt solid #111;width:6pt}.matrix-brackets:before{left:0}.matrix-brackets:after{left:auto;right:0}.matrix-brackets table{border-collapse:collapse;font-size:12pt;font-variant-numeric:tabular-nums}.matrix-brackets td{padding:2pt 5pt;text-align:center;white-space:nowrap}.matrix-pair{display:flex;justify-content:space-evenly;align-items:flex-start;gap:12pt;break-inside:avoid}.matrix-pair>.matrix-figure{max-width:49%;flex:0 1 auto}.data-table{break-inside:auto}.data-table table{border-collapse:collapse;margin:0 auto;max-width:100%;width:auto;font-size:11.5pt;text-align:center}.data-table th,.data-table td{border:.55pt solid #555;padding:3pt 5pt;overflow-wrap:anywhere}.data-table th{background:#f2f2f2;font-weight:bold}.data-table tr{break-inside:avoid}.data-table thead{display:table-header-group}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:10.5pt/1.4 Consolas,monospace;break-inside:avoid}.references{font-size:10.5pt;border-top:.5pt solid #aaa;margin-top:18pt;padding-top:5pt}.references h3{font-size:11pt;margin:5pt 0}.references ul{padding-left:15pt;margin:5pt 0}.cover{padding:40mm 8mm 0}.cover h1{font-size:28pt}.cover h2{font-size:20pt}.cover p{font-size:15pt;line-height:1.7}.cover .byline{margin-top:35pt;font-size:12pt;color:#444}
`;
export const sizingCss=`body{width:178mm}p{overflow-wrap:anywhere}.matrix-figure{font-size:12pt}.matrix-brackets table{font-size:inherit}.data-table{font-size:11.5pt}.data-table table{font-size:inherit}.table-note{font-size:11pt;font-style:italic}`;
