'use strict';
// All sources and anatomy are purpose-built synthetic fixtures, not extracted clinical data.
const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const KEY = 'prostapaper-review-demo-v1';
const fresh = () => ({version:1, selected:'L1', decisions:{}, status:'draft', history:[], final:null});
let state = fresh(), filter = 'all', expanded = 'location', zoom = 100, action = null;
try { const saved = JSON.parse(localStorage.getItem(KEY)); if(saved?.version === 1 && saved.decisions && Array.isArray(saved.history) && ['draft','approved','refused'].includes(saved.status)) state = {...fresh(), ...saved}; } catch (_) { /* Storage may be unavailable for file URLs. */ }
const issues = [
 {id:'location', title:'L1 · Anterior / posterior location conflict', type:'Conflict', blocking:true, lesion:'L1', report:'Right anterior peripheral-zone focus (report lines 1–3).', diagram:'Posterior-region outlines across base, mid and apex. Diagram side is assigned from the report, not independent corroboration.', detail:'The identity match is plausible, but location remains disputed. Choosing a source changes only the combined interpretation; both source statements remain available.'},
 {id:'identity', title:'L2 · Diagram correspondence uncertain', type:'Uncertainty', blocking:false, lesion:'L2', report:'A second right anterior focus is described. Longitudinal level is not reported.', diagram:'One small anterior mark is visible in the mid panel; its link to L2 is provisional.', detail:'Acknowledge the uncertainty without turning this into an accepted match or inventing longitudinal extent.'},
 {id:'unmatched', title:'M1 · Unmatched mark needs interpretation', type:'Unmatched mark', blocking:false, lesion:'M1', report:'No established corresponding report subject.', diagram:'Small isolated pencil-like stroke in the apex panel. Its meaning is unknown.', detail:'This mark does not create a third lesion and is not assigned a grade. It remains unresolved after acknowledgement.'}
];
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function notify(text) { $('#toast').textContent=text; clearTimeout(notify.timer); notify.timer=setTimeout(()=>$('#toast').textContent='',4500); }
function persist() { try { localStorage.setItem(KEY,JSON.stringify(state)); return true; } catch (_) { notify('Browser storage unavailable. This review remains in memory for this tab only.'); return false; } }
function log(text, reviewer, reason) { state.history.push({at:new Date().toISOString(),text,reviewer,reason}); }
function locationValue() { const d=state.decisions.location; return d?.choice==='report' ? 'Right anterior peripheral zone — report interpretation adopted' : d?.choice==='diagram' ? 'Right posterior peripheral zone — diagram interpretation adopted' : 'Unresolved: anterior (report) / posterior (diagram)'; }
function diagram(source) {
 let shapes='';
 ['Base','Mid','Apex'].forEach((name,i)=>{
  const x=92+i*165;
  shapes+=`<g transform="translate(${x} 90)"><text class="view-title" text-anchor="middle" y="-65">${name}</text><path class="organ" d="M0 -46 C-75 -57 -82 35 -37 47 Q0 60 37 47 C82 35 75 -57 0 -46Z"/><ellipse cx="0" cy="6" rx="25" ry="31" class="sector-line"/><path class="sector-line" d="M0 -46V53 M-65 4H65 M-45 -32L44 40 M45 -32L-44 40"/><text class="diagram-text" y="-31" x="-55">A</text><text class="diagram-text" y="40" x="49">P</text></g>`;
  // Clean view depicts competing categorical sectors, not invented calibrated contours.
  const anterior=!source && state.decisions.location?.choice==='report';
  const y=anterior?68:116;
  shapes+=`<ellipse data-lesion="L1" role="button" tabindex="0" aria-label="Select L1 in ${name}; Grade Group 3, ${anterior?'adopted anterior location':'posterior diagram interpretation'}" class="mark ${!source&&!state.decisions.location?'provisional':''} ${state.selected==='L1'?'selected':''}" cx="${x-38}" cy="${y}" rx="17" ry="13" fill="${source?'none':'#b69acf'}" stroke="${source?'#b55486':'#8765a3'}"/><text class="mark-label" x="${x-46}" y="${y+4}">${source?'a'+(i+1):'L1'}</text>`;
  if(!source&&!state.decisions.location) shapes+=`<ellipse cx="${x-38}" cy="65" rx="17" ry="13" fill="none" stroke="#8765a3" stroke-dasharray="2 3"/><text class="diagram-text" x="${x-48}" y="48">L1?</text>`;
 });
 shapes+=`<ellipse data-lesion="L2" role="button" tabindex="0" aria-label="Select L2, Grade Group 1, provisional correspondence" class="mark provisional ${state.selected==='L2'?'selected':''}" cx="274" cy="64" rx="9" ry="8" stroke="${source?'#b55486':'#327d70'}" fill="${source?'none':'#71baae'}"/><text class="mark-label" x="287" y="62">${source?'b1':'L2?'}</text><path data-lesion="M1" role="button" tabindex="0" aria-label="Select unmatched mark M1, not an established lesion" class="mark provisional ${state.selected==='M1'?'selected':''}" d="M447 113l9 10-3 7" fill="none" stroke="#636f6a"/><text class="mark-label" x="460" y="126">M1?</text>`;
 return `<svg viewBox="0 0 515 185" role="group" aria-label="${source?'Synthetic source diagram':'Combined schematic, categorical locations only'}"><text class="diagram-text" x="20" y="174">${source?'a1–a3: pink outlines · b1: small mark · M1: pencil stroke':'A: anterior · P: posterior · patient side assigned from report'}</text>${shapes}</svg>`;
}
function select(id) { state.selected=id; render(); }
function showEvidence(id) { const el=$('#evidence-'+id); if(el) el.scrollIntoView({behavior:'auto',block:'center'}); else notify('M1 has no established report counterpart; inspect the source diagram.'); }
function renderFinding() {
 const id=state.selected;
 if(id==='M1') { $('#finding-card').innerHTML='<h3>M1 · Unmatched source mark</h3><div class="card-tags"><span class="pill warn">Meaning unresolved</span><span class="pill muted">Grade unknown</span></div><p>A source mark, not an established tumour. No additional lesion is inferred from this mark. Acknowledgement preserves the uncertainty.</p><button data-open-issue="unmatched">Review mark uncertainty</button>'; return; }
 const isL1=id==='L1';
 $('#finding-card').innerHTML=`<h3>${id} · ${isL1?'Proposed dominant focus':'Second report-described focus'} <span class="grade ${isL1?'g3':'g1'}">ISUP GG${isL1?'3':'1'}</span></h3><div class="card-tags"><span class="pill muted">${isL1?'Provisional grouping across 3 panels':'Diagram correspondence provisional'}</span><span class="pill warn">${isL1&&!state.decisions.location?'Location conflict':isL1?'Location decision recorded':'Identity uncertain'}</span></div><dl><div class="property"><dt>Location</dt><dd>${isL1?locationValue():'Right anterior; level not reported'}<br><button data-open-issue="${isL1?'location':'identity'}">Inspect comparison</button></dd></div><div class="property"><dt>Dimensions</dt><dd>${isL1?'≈ 11 × 15 × 8 mm; axes unspecified':'≈ 3 mm diameter'} <span class="badge">Report only</span></dd></div><div class="property"><dt>Grade</dt><dd>GG${isL1?'3 · Gleason 4 + 3 = 7':'1 · Gleason 3 + 3 = 6'} <span class="badge">Report only</span></dd></div><div class="property"><dt>Assessment</dt><dd>${isL1?'Location assessed separately from size and grade.':'Source-supported focus; diagram match is not confirmed.'} Certainty unassessed.</dd></div></dl><button data-evidence="${id}">Show report evidence ↗</button><p class="small">No physical scale is inferred. Source ink colour does not determine grade.</p>`;
}
function renderIssues() {
 const visible=issues.filter(i=>filter==='all'||(filter==='open'?!state.decisions[i.id]:!!state.decisions[i.id]));
 $('#issue-list').innerHTML=visible.map(i=>{ const d=state.decisions[i.id]; return `<article class="issue ${d?'resolved':''}" id="issue-${i.id}"><button class="issue-top" data-expand="${i.id}" aria-expanded="${expanded===i.id}" aria-controls="body-${i.id}"><span>${d?'✓':'⚠'} ${i.title}</span><span class="pill ${d?'good':'warn'}">${d?(i.blocking?'Decision recorded':'Acknowledged · unresolved'):(i.blocking?'Blocking conflict':i.type)}</span></button><div class="issue-body" id="body-${i.id}" ${expanded===i.id?'':'hidden'}><p>${i.detail}</p><div class="compare"><div><strong>Report input</strong><p>${i.report}</p></div><div><strong>Diagram input</strong><p>${i.diagram}</p></div></div>${d?`<div class="decision-note"><strong>${escapeHtml(d.label)}</strong><br>${escapeHtml(d.reviewer)} · ${escapeHtml(d.reason)}</div>`:''}<button data-decide="${i.id}" ${state.status!=='draft'?'disabled':''}>${d?'Change decision':i.blocking?'Review competing interpretations':'Acknowledge and retain uncertainty'}</button> <button data-evidence="${i.lesion}">Show source evidence</button></div></article>`; }).join('')||'<p>No issues in this filter.</p>';
}
function render() {
 const locked=state.status!=='draft', blocking=!state.decisions.location, open=issues.filter(i=>!state.decisions[i.id]).length;
 $('#source-diagram').innerHTML=diagram(true); $('#clean-diagram').innerHTML=diagram(false);
 $('#issue-summary').textContent=`${blocking?'1 blocking conflict':'No blocking conflicts'} · 2 uncertainties${open?' · '+open+' unaddressed':' · all addressed'}`;
 $('#review-status').textContent=state.status==='approved'?'Approved with limitations':state.status==='refused'?'Refused':'Not reviewed';
 $('#review-status').className='pill '+(state.status==='approved'?'good':state.status==='refused'?'bad':'warn');
 $('#decision-summary').textContent=state.final?`${state.final.reviewer} · ${new Date(state.final.at).toLocaleString()}`:'Your decisions stay in this browser.';
 $('#footer-state').textContent=locked?'Review decision recorded':'Review in progress';
 $('#approve').disabled=locked||blocking; $('#approve').title=blocking?'Record a location decision before approving.':''; $('#refuse').disabled=locked; $('#reopen').hidden=!locked;
 $$('[data-lesion]').forEach(el=>{ el.classList.toggle('selected',el.dataset.lesion===state.selected); if(el.tagName==='BUTTON') el.setAttribute('aria-pressed',String(el.dataset.lesion===state.selected)); });
 renderFinding(); renderIssues();
 $('#audit-count').textContent=`(${state.history.length})`;
 $('#audit-list').innerHTML=state.history.map(h=>`<li><strong>${escapeHtml(h.text)}</strong> · ${escapeHtml(h.reviewer)} · ${escapeHtml(new Date(h.at).toLocaleString())}<br>${escapeHtml(h.reason)}</li>`).join('')||'<li>No decisions recorded yet.</li>';
}
function openDialog(type,id) {
 if(type!=='reopen'&&state.status!=='draft') return;
 action={type,id}; $('#action-form').reset(); $('#reviewer').value=state.final?.reviewer||state.history.at(-1)?.reviewer||'';
 const issue=issues.find(i=>i.id===id);
 $('#dialog-title').textContent=type==='issue'?issue.title:type==='approve'?'Approve this summary':type==='reopen'?'Reopen this review':'Refuse this entry';
 $('#dialog-description').textContent=type==='issue'?issue.detail:type==='approve'?'Approve synthetic assessment revision 1, including the provisional grouping, unresolved L2 correspondence and unmatched M1 mark. Grade and dimensions remain report-only. This does not submit data anywhere.':type==='reopen'?'The previous decision remains in history. Editing makes a new review necessary.':'Record why this summary is not acceptable. Source evidence and all prior decisions will be retained.';
 $('#dialog-options').innerHTML=type==='issue'&&issue.blocking?'<label for="choice">Combined location interpretation</label><select id="choice" required><option value="">Choose an interpretation</option><option value="report">Adopt report: anterior</option><option value="diagram">Adopt diagram: posterior</option><option value="unresolved">Keep unresolved (approval remains blocked)</option></select>':'';
 $('#ack-label').hidden=type!=='approve'; $('#ack').required=type==='approve'; $('#action-dialog').showModal(); $('#reviewer').focus();
}
document.addEventListener('click',e=>{
 const el=e.target.closest('[data-lesion],[data-open-issue],[data-expand],[data-decide],[data-evidence],[data-filter]'); if(!el)return;
 if(el.dataset.lesion) select(el.dataset.lesion);
 if(el.dataset.evidence) { select(el.dataset.evidence); showEvidence(el.dataset.evidence); }
 if(el.dataset.expand) { expanded=expanded===el.dataset.expand?null:el.dataset.expand;renderIssues(); }
 if(el.dataset.openIssue) {filter='all'; expanded=el.dataset.openIssue;setFilterButtons();renderIssues();$('#issue-'+expanded).scrollIntoView({block:'center'});}
 if(el.dataset.decide)openDialog('issue',el.dataset.decide);
 if(el.dataset.filter) {filter=el.dataset.filter;setFilterButtons();renderIssues();}
});
document.addEventListener('keydown',e=>{if(e.target.matches('svg [data-lesion]')&&['Enter',' '].includes(e.key)){e.preventDefault();select(e.target.dataset.lesion);}});
function setFilterButtons() { $$('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===filter))); }
$('#next-issue').onclick=()=>{const i=issues.find(i=>!state.decisions[i.id]);if(!i)return notify('All issues addressed. Two acknowledged uncertainties still remain.');filter='all';expanded=i.id;setFilterButtons();renderIssues();$('#issue-'+i.id).scrollIntoView({block:'center'});};
$('#zoom-in').onclick=()=>setZoom(Math.min(200,zoom+25)); $('#zoom-out').onclick=()=>setZoom(Math.max(75,zoom-25));
function setZoom(value){zoom=value;$('#source-sheet').style.width=zoom+'%';$('#zoom-value').textContent=zoom+'%';}
$('#approve').onclick=()=>{if(state.decisions.location)openDialog('approve');}; $('#refuse').onclick=()=>openDialog('refuse'); $('#reopen').onclick=()=>openDialog('reopen');
$('#cancel-dialog').onclick=()=>$('#action-dialog').close();
$('#action-form').onsubmit=e=>{
 e.preventDefault();const reviewer=$('#reviewer').value.trim(),reason=$('#reason').value.trim();if(!reviewer||!reason)return notify('Enter a reviewer name and a meaningful reason.');
 const at=new Date().toISOString();
 if(action.type==='issue'){
  const i=issues.find(i=>i.id===action.id),choice=i.blocking?$('#choice').value:'acknowledge';
  if(choice==='unresolved'){delete state.decisions[i.id];log('Location retained as unresolved',reviewer,reason);}
  else {const label=choice==='report'?'Report location adopted; diagram counterevidence retained':choice==='diagram'?'Diagram location adopted; report counterevidence retained':'Uncertainty acknowledged, not resolved';state.decisions[i.id]={choice,label,reviewer,reason,at};log(label,reviewer,reason);}
 } else if(action.type==='reopen'){log('Review reopened; prior approval/refusal superseded',reviewer,reason);state.status='draft';state.final=null;}
 else {if(action.type==='approve'&&(!state.decisions.location||!$('#ack').checked))return;state.status=action.type==='approve'?'approved':'refused';state.final={reviewer,reason,at};log(state.status==='approved'?'Summary approved with stated limitations':'Entry refused',reviewer,reason);}
 $('#action-dialog').close();persist();render();notify('Decision recorded locally. No data submitted.');
};
$('#save').onclick=()=>{if(persist())notify('Draft and decision history saved in this browser. No data submitted.');};
$('#reset').onclick=()=>{if(confirm('Clear all local demo decisions and restore the synthetic fixture?')){state=fresh();filter='all';expanded='location';persist();setFilterButtons();render();notify('Demo reset.');}};
render();
