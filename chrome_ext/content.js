console.log('content js loaded')


function productsObject(aa){
  for(var i=0; i<=aa.length;i++){
  var idx;
  var startIdx;
  var endIdx;
      if(aa[i].text.includes(`window.runParams = {"`)){
          idx=i;
          startIdx=aa[i].text.indexOf(`{"resultCount":`);
          endIdx=aa[i].text.indexOf(`                window.runParams.csrfToken = '11y6gl1azhznx';`)-2;
          jsn = JSON.parse(aa[i].innerText.slice(startIdx,endIdx)).items;
          return(jsn);
      }
  }
  return null;
}

function prds(prdsObj){
products = {}
for(prd in prdsObj){
  products[prdsObj[prd].productId]=prdsObj[prd].title
  console.log(prdsObj[prd].title)
}
return(products)
}


aa=document.getElementsByTagName("script")
bb=productsObject(aa)
snd=prds(bb)
s=btoa(JSON.stringify(snd))
u='http://127.0.0.1:8000/save-products/'+s+'/'
url=encodeURI(u)
window.open(url,"_self")