// ==UserScript==
// @name         National Health Commission COVID-19 Update Extractor
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Extract key information about COVID-19 trend
// @author       You
// @match        *://www.nhc.gov.cn/xcs/yqtb/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=greasyfork.org
// @grant        none
// ==/UserScript==

const provi_regexp = /(?<prov_name>\p{Lo}+)(?<prov_count>\d+)例/u;
const nhc_para_spec = [
    {
        id:"确诊",
        h: /\d{1,2}月\d{1,2}日0—24时，31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例(\d+)例/u,
        d: [
            {
                id: "输入",
                h: /其中境外输入病例(?<总计>\d+)例\p{Ps}(?<分省>(?:\p{Lo}+\d+例，?)+)\p{Pe}(?:，含(?<无症状归转总计>\d)例由无症状感染者转为确诊病例\p{Ps}(?<无症状归转分省>(?:在\p{Lo}+)|(?:\p{Lo}+\d+例，?)+)\p{Pe})?/u,
            },
            {
                id: "本土",
                h: /本土病例(?<总计>\d+)例\p{Ps}(?<分省>(?:\p{Lo}+\d+例，?)+)\p{Pe}(?:，含(?<无症状归转总计>\d+)例由无症状感染者转为确诊病例\p{Ps}(?<无症状归转分省>(?:在\p{Lo}+)|(?:\p{Lo}+\d+例，?)+)\p{Pe})?/u,
            },
            /*{
                id: "疑似",
                h: /新增疑似病例(?<总计>\d+)例，(?<疑似病例情况>[^\u3002])。/u, // http://www.nhc.gov.cn/xcs/yqtb/202203/8a138fb1f4bf409c9e81bcbc5f30db0e.shtml 新增疑似病例5例，其中境外输入病例2例（均在上海），本土病例3例（均在上海）
            },*/
        ]
    },
    {
        id:"无症状",
        h: /31个省（自治区、直辖市）和新疆生产建设兵团报告新增无症状感染者(\d+)例/u,
        d: [
            {
                id: "输入",
                h: /其中境外输入(?<总计>\d+)例/u,
            },
            {
                id: "本土",
                h: /本土(?<总计>\d+)例\p{Ps}(?<分省>(?:\p{Lo}+\d+例，?)+)\p{Pe}/u,
            },
        ]
    },
];

/* ((\p{Lo}+)(\d+)例，?)+, Lo: Letter, other
see https://en.wikipedia.org/wiki/Unicode_character_property */


function nhcToSpreadsheet(x) {
    let o = new Object();
    o["本土确诊_全国"] = x["确诊"]["本土"]["总计"];
    o["本土无症状转确诊_全国"] = x["确诊"]["本土"]["无症状归转总计"];
    o["本土确诊_上海"] = x["确诊"]["本土"]["分省"]["上海"];

    o["本土无症状_全国"] = x["无症状"]["本土"]["总计"];
    o["本土无症状_上海"] = x["无症状"]["本土"]["分省"]["上海"];

    o["输入确诊_全国"] = x["确诊"]["输入"]["总计"];
    o["输入无症状转确诊_全国"] = x["确诊"]["输入"]["无症状归转总计"];
    o["输入无症状_全国"] = x["无症状"]["输入"]["总计"];
    return o;
}

(function() {
    'use strict';

    let nhc_report_title_div = document.querySelector('div.tit');
    if (!nhc_report_title_div) return;

    nhc_report_title_div.appendChild(document.createElement('br'));

    let txt_area_clipboard = document.createElement('textarea');
    txt_area_clipboard.setAttribute('id', 'forCopying');
    txt_area_clipboard.setAttribute('cols', '45');
    txt_area_clipboard.setAttribute('rows', '10');
    txt_area_clipboard.setAttribute('spellcheck', 'false');
    let txt_area_tosheet = document.createElement('textarea');
    txt_area_tosheet.setAttribute('id', 'forCopying');
    txt_area_tosheet.setAttribute('cols', '45');
    txt_area_tosheet.setAttribute('rows', '10');
    txt_area_tosheet.setAttribute('spellcheck', 'false');

    let nhc_report_paragraphs = document.querySelector('div#xw_box').innerText.split('\n').filter(i => i);

    let parsedResult = new Object();

    for (let curr_para of nhc_report_paragraphs) {

        for (const [specIdx, specContent] of nhc_para_spec.entries()) {
            if (curr_para.match(specContent.h)) {
                parsedResult[specContent.id] = new Object();

                for (const detailedSpec of specContent.d) {
                    parsedResult[specContent.id][detailedSpec.id] = new Object();
                    let detail_matched = curr_para.match(detailedSpec.h).groups;
                    for (const [key, value] of Object.entries(detail_matched)) {
                        if (!value) {
                            parsedResult[specContent.id][detailedSpec.id][key] = 0;
                        }
                        else if (key.includes('总计')) {
                            parsedResult[specContent.id][detailedSpec.id][key] = parseInt(value);
                        }
                        else if (key.includes('分省')) {
                            let prov_list = value.split('，');

                            if (prov_list.length > 1) {
                                prov_list = prov_list.map(x => x.match(provi_regexp).groups);
                                parsedResult[specContent.id][detailedSpec.id][key] = prov_list.reduce((obj, item) => (obj[item.prov_name] = parseInt(item.prov_count), obj) ,{});
                            } else {
                                parsedResult[specContent.id][detailedSpec.id][key] = new Object();
                                parsedResult[specContent.id][detailedSpec.id][key][prov_list.pop().substring(1)] = 1;
                            }
                        }
                    }
                }
                break;
            };
        }
    }

    txt_area_clipboard.value = JSON.stringify(parsedResult, null, 4);
    txt_area_tosheet.value = JSON.stringify(nhcToSpreadsheet(parsedResult), null, 4);

    nhc_report_title_div.appendChild(txt_area_clipboard);
    nhc_report_title_div.appendChild(txt_area_tosheet);
})();
