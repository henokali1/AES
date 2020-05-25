console.log('content js loaded')


tot_sales_last = 0
function productsObject(aa){
  for(var i=0; i<=aa.length;i++){
  var idx;
  var startIdx;
  var endIdx;
      if(aa[i].text.includes(`window.runParams = {"`)){
          idx=i;
          startIdx=aa[i].text.indexOf(`{"resultCount":`);
          endIdx=aa[i].text.indexOf(`"resultType":"normal_result"}`)+29;
          // console.log(aa[i].innerText.slice(startIdx,endIdx))
          jsn = JSON.parse(aa[i].innerText.slice(startIdx,endIdx)).items;
          return(jsn);
      }
  }
  return null;
}

function prds(prdsObj){
cntr=0
products = {}
for(prd in prdsObj){
  units_sold = parseInt(prdsObj[prd].tradeDesc.split(' ')[0])
  products[cntr] = {'aes_id':prdsObj[prd].productId, 'title':prdsObj[prd].title, 'units_sold':units_sold}
  tot_sales_last = units_sold
  cntr += 1
  // products[prdsObj[prd].productId]=prdsObj[prd].title
}
return(products)
}

function saveJSON(data, filename){

  if(!data) {
      console.error('No data')
      return;
  }

  if(!filename) filename = 'console.json'

  if(typeof data === "object"){
      data = JSON.stringify(data, undefined, 4)
  }

  var blob = new Blob([data], {type: 'text/json'}),
      e    = document.createEvent('MouseEvents'),
      a    = document.createElement('a')

  a.download = filename
  a.href = window.URL.createObjectURL(blob)
  a.dataset.downloadurl =  ['text/json', a.download, a.href].join(':')
  e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
  a.dispatchEvent(e)
}

aa=document.getElementsByTagName("script")
bb=productsObject(aa)
snd=prds(bb)
saveJSON(snd,'s.json')


// aa=document.getElementsByTagName("script")
// bb=productsObject(aa)
// snd=prds(bb)
// s=btoa(JSON.stringify(snd))
u='http://127.0.0.1:8000/save-products/' + String(tot_sales_last) + '/'
url=encodeURI(u)
window.open(url,"_self")