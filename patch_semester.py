from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '<div id="lapBadge" class="hidden mt-1 inline-block bg-blue-500 text-white text-sm font-bold px-3 py-1 rounded-full">'
insert = '''<div class="mt-3 inline-flex rounded-full bg-gray-100 p-1 shadow-inner" id="semesterSwitch">
    <button id="frontSemesterBtn" onclick="switchSemester('front')" class="px-5 py-2 rounded-full font-bold text-sm md:text-base transition-all">前期</button>
    <button id="backSemesterBtn" onclick="switchSemester('back')" class="px-5 py-2 rounded-full font-bold text-sm md:text-base transition-all">後期</button>
</div>
'''
if 'id="semesterSwitch"' not in s:
    s = s.replace(marker, insert + marker, 1)

s = s.replace('<span class="text-2xl md:text-3xl text-gray-600">（前期）</span>', '<span id="semesterTitle" class="text-2xl md:text-3xl text-gray-600">（前期）</span>', 1)

back = '''        <div id="backSection" class="hidden">
            <div class="overflow-x-auto mb-8">
                <table class="test-table w-full bg-white text-center text-lg">
                    <thead><tr class="bg-blue-100">
                        <th class="py-3 px-2 w-24">級</th>
                        <th class="py-3 px-2 w-1/6">13</th><th class="py-3 px-2 w-1/6">14</th><th class="py-3 px-2 w-1/6">15</th>
                        <th class="py-3 px-2 w-1/6">16</th><th class="py-3 px-2 w-1/6">17</th><th class="py-3 px-2 w-1/6">18</th>
                    </tr></thead><tbody id="backTableBody1"></tbody>
                </table>
            </div>
            <div class="overflow-x-auto mb-8">
                <table class="test-table w-full bg-white text-center text-lg">
                    <thead><tr class="bg-blue-100">
                        <th class="py-3 px-2 w-24">級</th>
                        <th class="py-3 px-1 w-1/6">19</th><th class="py-3 px-1 w-1/6">20</th><th class="py-3 px-1 w-1/6">21</th>
                        <th class="py-3 px-1 w-1/6">22</th><th class="py-3 px-1 w-1/6">23</th><th class="py-3 px-1 w-1/6">24</th>
                    </tr></thead><tbody id="backTableBody2"></tbody>
                </table>
            </div>
        </div>

'''
if 'id="backSection"' not in s:
    s = s.replace('        <!-- 全クリアバナー -->', back + '        <!-- 全クリアバナー -->', 1)

controller = r'''<script>
(function(){
    const SEM_KEY='kanjiSemester';
    let currentSemester=localStorage.getItem(SEM_KEY)||'front';
    const range=()=>currentSemester==='front'?[1,12]:[13,24];
    const keys=()=>currentSemester==='front'?['kanjiPassedDates','kanjiLap1Records','kanjiLap']:['kanjiLatePassedDates','kanjiLateLap1Records','kanjiLateLap'];
    const load=()=>{const [a,b,c]=keys();state.passedDates=JSON.parse(localStorage.getItem(a)||'{}');state.lap1Records=new Set(JSON.parse(localStorage.getItem(b)||'[]'));state.lap=parseInt(localStorage.getItem(c)||'1');};
    const save=()=>{const [a,b,c]=keys();localStorage.setItem(a,JSON.stringify(state.passedDates));localStorage.setItem(b,JSON.stringify([...state.lap1Records]));localStorage.setItem(c,String(state.lap));};

    window.saveData=save;
    window.isPassed=id=>!!state.passedDates[id];
    window.isLap1=id=>state.lap1Records.has(id);
    window.passedList=()=>Object.keys(state.passedDates);
    window.calcUnlocked=()=>{const [min,max]=range(),u=new Set([`level-1-kyu-${min}`]);passedList().forEach(id=>{const m=id.match(/level-(\d+)-kyu-(\d+)/);if(!m)return;const l=+m[1],k=+m[2];if(l===1){u.add(`level-2-kyu-${k}`);if(k<max)u.add(`level-1-kyu-${k+1}`)}else if(l===2)u.add(`level-3-kyu-${k}`);else if(l===3&&k<max)u.add(`level-1-kyu-${k+1}`);u.add(id)});return u};
    window.isUnlocked=id=>calcUnlocked().has(id);
    window.isKyuAllCleared=k=>[1,2,3].every(l=>isPassed(`level-${l}-kyu-${k}`));
    window.isLevelAllCleared=l=>{const [min,max]=range();return Array.from({length:max-min+1},(_,i)=>i+min).every(k=>isPassed(`level-${l}-kyu-${k}`));};

    const badgeMap={1:['fire','炎'],2:['water','水'],3:['nature','自然'],4:['thunder','雷'],5:['ice','氷'],6:['shadow','影'],7:['gravity','重力'],8:['wind','風'],9:['earth','大地'],10:['light','光'],11:['moon','月'],12:['psychic','エスパー']};
    const badge=(k,l)=>{const [slug,name]=badgeMap[((k-1)%12)+1];return{name,url:`https://tt-sensei.github.io/edu-assets/assets/web/elements/${slug}/level-${l}/badge.webp`};};

    window.generateTable=function(tbodyId,startKyu){const tbody=document.getElementById(tbodyId);if(!tbody)return;tbody.innerHTML='';['レベル１','レベル２','レベル３'].forEach((name,li)=>{const l=li+1,lc=isLevelAllCleared(l),tr=document.createElement('tr'),th=document.createElement('th');th.className='py-3 px-2 bg-orange-50';if(lc)th.classList.add('row-cleared');th.textContent=name;tr.appendChild(th);for(let i=0;i<6;i++){const k=startKyu+i,id=`level-${l}-kyu-${k}`,b=badge(k,l),un=isUnlocked(id),pass=isPassed(id),lap1=isLap1(id),kc=isKyuAllCleared(k),td=document.createElement('td');td.className='p-0 cursor-pointer hover:bg-orange-100 transition-colors duration-200';if(kc&&lc)td.classList.add('both-cleared');else if(kc)td.classList.add('col-cleared');else if(lc)td.classList.add('row-cleared');if(state.lap===2&&lap1&&!pass)td.classList.add('lap2-cell');const ext=currentSemester==='front'?'jpg':'png';td.onclick=()=>openModal(id,k,name,`kanji_test_${l}`,`${k}.${ext}`,b.name,l);if(selectedCellIds.has(id))td.classList.add('cell-selected');const cls=!un?'item-locked':pass?((state.lap===2&&lap1)?'item-passed-lap2':'item-passed do-pop'):'item-challenge';const icon=un?`<img class="element-badge" src="${b.url}" alt="${b.name}エレメント Lv.${l}">`:'🔒';td.innerHTML=`<div class="cell-content"><input class="cell-select" type="checkbox" aria-label="${k}級 レベル${l}を選択" ${selectedCellIds.has(id)?'checked':''} ${pass?'disabled':''} onclick="event.stopPropagation()" style="${bulkSelectMode?'':'display:none;'}" onchange="toggleCellSelection('${id}',this.checked)"><span class="item-icon ${cls}">${icon}</span><span class="item-date">${pass?state.passedDates[id]:''}</span></div>`;tr.appendChild(td)}tbody.appendChild(tr)})};

    window.refreshTable=function(){const f=currentSemester==='front';document.getElementById('frontSemesterBtn').className='px-5 py-2 rounded-full font-bold text-sm md:text-base transition-all '+(f?'bg-white text-orange-500 shadow':'text-gray-500');document.getElementById('backSemesterBtn').className='px-5 py-2 rounded-full font-bold text-sm md:text-base transition-all '+(!f?'bg-white text-blue-500 shadow':'text-gray-500');document.getElementById('semesterTitle').textContent=f?'（前期）':'（後期）';document.getElementById('frontSection').classList.toggle('hidden',!f);document.getElementById('backSection').classList.toggle('hidden',f);if(f){generateTable('tableBody1',1);generateTable('tableBody2',7)}else{generateTable('backTableBody1',13);generateTable('backTableBody2',19)}updateProgress();checkAllClear();};
    window.updateProgress=function(){const n=passedList().length;document.getElementById('progressText').textContent=`${n} / 36`;document.getElementById('progressBar').style.width=`${Math.min(100,n/36*100)}%`;};
    window.checkAllClear=function(){document.getElementById('allClearBanner').classList.toggle('hidden',passedList().length<36);};

    window.openModal=function(id,k,name,folder,file,emoji,l){currentCellId=id;currentKyu=k;currentLevel=l;currentEmoji=emoji;modalTitle.textContent=`${currentSemester==='front'?'前期':'後期'}・${k}級 - ${name}`;modalImage.style.display='none';imagePlaceholder.classList.add('hidden');modalImage.src='';applyPassButtonState();modalImage.onload=()=>{modalImage.style.display='block';imagePlaceholder.classList.add('hidden')};modal.classList.remove('hidden');modal.classList.add('flex');setTimeout(()=>{modalContent.classList.remove('scale-95','opacity-0');modalContent.classList.add('scale-100','opacity-100');modalImage.src=`${folder}/${file}`},10)};
    window.executePass=function(){state.passedDates[currentCellId]=todayStr();save();launchConfetti();refreshTable();closeModal()};
    window.executeCancel=function(){delete state.passedDates[currentCellId];save();refreshTable();closeModal()};
    window.executeBulkPass=function(){selectedCellIds.forEach(id=>state.passedDates[id]=todayStr());selectedCellIds.clear();save();launchConfetti();refreshTable()};
    window.checkPassword=function(){if(bulkPassMode){if(passwordInput.value==='8818'){closePasswordModal();executeBulkPass()}else{passwordError.classList.remove('hidden');passwordInput.value='';passwordInput.focus()}}else if(passwordInput.value===getPassword(currentKyu,currentLevel)){closePasswordModal();executePass()}else{passwordError.classList.remove('hidden');passwordInput.value='';passwordInput.focus()}};
    window.startLap2=function(){openConfirmModal(`${currentSemester==='front'?'前期':'後期'}を2周目にします！\n1周目の記録は色を変えて残ります。\nよろしいですか？`,()=>{state.lap1Records=new Set(passedList());state.passedDates={};state.lap=2;save();refreshTable()})};
    window.resetProgress=function(){openConfirmModal(`${currentSemester==='front'?'前期':'後期'}のクリア記録をすべて消去します。\n本当によろしいですか？`,()=>{keys().forEach(k=>localStorage.removeItem(k));location.reload()})};
    window.switchSemester=function(next){if(next===currentSemester)return;save();currentSemester=next;localStorage.setItem(SEM_KEY,next);load();selectedCellIds.clear();bulkSelectMode=false;document.getElementById('bulkPassButton').textContent='🛡️ 一括合格を選択';refreshTable()};

    const allClear=document.getElementById('allClearBanner');
    if(!document.getElementById('frontSection')){const w=document.createElement('div');w.id='frontSection';const tables=[...document.querySelectorAll('tbody#tableBody1,tbody#tableBody2')].map(x=>x.closest('.overflow-x-auto'));allClear.parentNode.insertBefore(w,allClear);tables.forEach(t=>w.appendChild(t));}
    load();refreshTable();
})();
</script>
'''

if 'const SEM_KEY=' not in s:
    s=s.replace('</body>',controller+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('patched',len(s))
