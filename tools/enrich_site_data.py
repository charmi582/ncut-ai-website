import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_JSON = ROOT / "data" / "site.json"


def main():
    data = json.loads(SITE_JSON.read_text(encoding="utf-8"))

    data["careerPaths"] = [
        {
            "title": "影像與視覺 AI",
            "items": ["影像演算法工程師", "電腦視覺工程師", "AI 影像辨識工程師", "自動光學檢測工程師"],
        },
        {
            "title": "智慧製造與 AIoT",
            "items": ["智慧製造系統開發", "智慧檢測系統開發", "AIoT 應用工程師", "機器人整合應用工程師"],
        },
        {
            "title": "資料科學與生成式 AI",
            "items": ["資料科學家", "生成式 AI 應用開發", "MLOps Engineer", "資訊安全與模型監控工程師"],
        },
    ]

    data["curriculumModules"] = [
        {
            "title": "智慧影像課程模組",
            "summary": "以影像處理、影像生成、影像辨識與影像分析為核心，銜接電腦視覺、AOI 與智慧製造檢測應用。",
            "focus": ["影像處理", "影像生成", "影像辨識", "影像分析"],
            "courses": ["影像處理", "電腦視覺", "人工智慧影像辨識", "深度學習應用", "智慧製造與檢測"],
            "outcomes": ["可投入電腦視覺、AI 影像辨識、自動光學檢測、智慧城市與安全監控等職務。"],
        },
        {
            "title": "智慧數據課程模組",
            "summary": "以資料探勘、特徵工程、資料生成、智慧資訊安全與模型資料飄移管理為核心，訓練資料驅動 AI 系統能力。",
            "focus": ["資料探勘", "特徵工程", "資料生成", "智慧資訊安全", "模型資料飄移管理"],
            "courses": ["資料科學", "機器學習", "大數據分析", "生成式 AI", "MLOps 與模型部署"],
            "outcomes": ["可投入資料科學、生成式 AI 應用、模型部署維運、智慧資訊安全與 AI 系統監控等職務。"],
        },
    ]

    data["labProfiles"] = [
        {
            "name": "智慧運算實驗室",
            "location": "國秀樓 2 樓 K216",
            "summary": "結合邊緣運算、資料工程、資料分析、資料科學、機器學習演算法與工控安全架構訓練。",
            "themes": ["邊緣運算", "資料工程", "機器學習", "工控安全"],
            "training": ["資料處理與分析實作", "AI 模型訓練與部署", "工業場域資料安全概念"],
        },
        {
            "name": "AI 物聯網實驗室",
            "location": "工具機大樓 4 樓 VA403",
            "summary": "結合智慧物聯網 AIoT，應用於智慧製造、智慧機械手臂與感測資料整合。",
            "themes": ["AIoT", "智慧製造", "感測資料", "機械手臂"],
            "training": ["物聯網資料擷取", "AIoT 系統整合", "智慧設備應用開發"],
        },
        {
            "name": "AI 機器人實驗室",
            "location": "國秀樓 3 樓 K305",
            "summary": "以 ROS 人工智慧發展實務、智慧穿戴、智慧搜索、智慧機器人與 AI 賽車訓練為主軸。",
            "themes": ["ROS", "智慧機器人", "智慧穿戴", "AI 賽車"],
            "training": ["機器人控制實務", "自主移動與感知", "AI 競賽與專題實作"],
        },
        {
            "name": "智慧影像實驗室",
            "location": "國秀樓 B1 樓 KB105",
            "summary": "發展醫療影像辨識、智慧城市、安全監控、工業自動化與品質檢測等影像 AI 應用。",
            "themes": ["醫療影像", "安全監控", "AOI", "品質檢測"],
            "training": ["影像資料標註與前處理", "電腦視覺模型訓練", "產線檢測應用"],
        },
        {
            "name": "智慧虛實實驗室",
            "location": "國秀樓 5 樓 K502",
            "summary": "發展 VR、AR、MR、虛實整合與沉浸式互動智慧應用。",
            "themes": ["VR", "AR", "MR", "沉浸式互動"],
            "training": ["虛實整合介面設計", "互動內容製作", "AI 與沉浸體驗應用"],
        },
        {
            "name": "鹿鳴台視聽教室",
            "location": "SOB114",
            "summary": "支援系所課程、專題發表、講座與跨域交流活動，作為教學展示與成果分享場域。",
            "themes": ["視聽教學", "專題發表", "講座活動", "成果展示"],
            "training": ["專題簡報", "技術展示", "跨域交流"],
        },
    ]

    data["studentResources"] = [
        {
            "title": "學分計畫表",
            "category": "課程規劃",
            "summary": "整理大學部修課架構與學分規劃，是學生安排四年課程與畢業檢核的主要依據。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-2380.php?Lang=zh-tw",
        },
        {
            "title": "課程地圖",
            "category": "課程規劃",
            "summary": "協助學生理解課程先後順序、能力養成路徑與系所專業模組的關聯。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-2381.php?Lang=zh-tw",
        },
        {
            "title": "課程綱要",
            "category": "課程規劃",
            "summary": "提供課程內容、授課方向與學習重點，便於學生選課與規劃自主學習。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-2407.php?Lang=zh-tw",
        },
        {
            "title": "實務專題",
            "category": "專題實作",
            "summary": "包含歷屆專題、專題影片、專題海報、實務專題時程與競賽辦法等資訊。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-8192.php?Lang=zh-tw",
            "children": [
                {"title": "歷屆專題", "href": "https://ai.ncut.edu.tw/p/405-1063-88468,c8192.php?Lang=zh-tw"},
                {"title": "實務專題時程", "href": "https://ai.ncut.edu.tw/p/405-1063-86109,c8192.php?Lang=zh-tw"},
                {
                    "title": "實務專題課程實施與專題製作競賽辦法",
                    "href": "https://ai.ncut.edu.tw/p/405-1063-86110,c8192.php?Lang=zh-tw",
                },
            ],
        },
        {
            "title": "畢業門檻",
            "category": "畢業檢核",
            "summary": "日間部四技學生至少應修滿 130 學分，並依入學年度檢核英文能力、自主學習與通識領域要求。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-2408.php?Lang=zh-tw",
            "children": [
                {"title": "畢業門檻明細", "href": "https://ai.ncut.edu.tw/p/405-1063-89115,c2408.php?Lang=zh-tw"},
                {"title": "畢業門檻規章及辦法", "href": "https://nmsd.ncut.edu.tw/wbcmss/Graduate"},
            ],
        },
        {
            "title": "核心證照",
            "category": "畢業檢核",
            "summary": "彙整系上認列之核心證照資訊，供學生準備專業證照與能力檢核。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-8129.php?Lang=zh-tw",
        },
        {
            "title": "校外實習",
            "category": "產業實務",
            "summary": "提供校外實習相關資訊，銜接學生產業實作、職場體驗與就業準備。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-8128.php?Lang=zh-tw",
        },
        {
            "title": "課程抵免",
            "category": "學務流程",
            "summary": "提供課程抵免申請資訊，協助轉學生、重修或具相關修課經驗學生辦理抵免。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-8267.php?Lang=zh-tw",
        },
        {
            "title": "系學會",
            "category": "學生組織",
            "summary": "系學會資訊與學生活動入口，連結學生自治、系上活動與同儕交流。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-2414.php?Lang=zh-tw",
        },
        {
            "title": "系友會",
            "category": "學生組織",
            "summary": "系友會資訊與畢業系友連結，協助維繫系友網絡與職涯交流。",
            "href": "https://n063.ncut.edu.tw/p/412-1063-2415.php?Lang=zh-tw",
        },
    ]

    data["specialPrograms"] = [
        {
            "slug": "industry-program",
            "title": "產學攜手合作專班",
            "summary": "整合學校課程、產業實作與合作廠商訓練，提供學生技職銜接與就業導向培育路徑。",
            "links": [
                {"title": "產攜班招生訊息", "type": "招生入口", "href": "https://industry.ncut.edu.tw/web/index.html"},
                {
                    "title": "112 學年度智慧科技應用製造專班學分計畫表",
                    "type": "PDF",
                    "href": "https://oaa.ncut.edu.tw/var/file/9/1009/attach/38/pta_65513_4369440_35469.pdf",
                },
                {
                    "title": "113 學年度半導體封測產攜專班學分計畫表",
                    "type": "PDF",
                    "href": "https://oaa.ncut.edu.tw/var/file/9/1009/attach/40/pta_67478_9100620_69847.pdf",
                },
                {
                    "title": "產學攜手合作專班原始頁面",
                    "type": "原系網",
                    "href": "https://n063.ncut.edu.tw/p/412-1063-8062.php?Lang=zh-tw",
                },
            ],
        },
        {
            "slug": "overseas-youth",
            "title": "海外青年技術訓練班",
            "summary": "提供海外青年技術訓練與產學合作課程資訊，聚焦半導體製造實務技術與技職專業養成。",
            "links": [
                {
                    "title": "海青班招生訊息",
                    "type": "招生入口",
                    "href": "https://recruit.ncut.edu.tw/p/406-1033-70888,r1131.php?Lang=zh-tw",
                },
                {
                    "title": "僑委會服務專線",
                    "type": "外部資源",
                    "href": "https://www.ocac.gov.tw/OCAC/Pages/Detail.aspx?nodeid=618&pid=507599",
                },
                {
                    "title": "僑委會緊急通報",
                    "type": "外部資源",
                    "href": "https://www.ocac.gov.tw/OCAC/Pages/VDetail.aspx?nodeid=4492&pid=13193977",
                },
                {
                    "title": "112 學年度半導體製造實務技術專班學分計畫表",
                    "type": "PDF",
                    "href": "https://oaa.ncut.edu.tw/var/file/9/1009/attach/38/pta_65512_1114416_35469.pdf",
                },
                {
                    "title": "113 學年度半導體製造實務技術專班學分計畫表",
                    "type": "PDF",
                    "href": "https://oaa.ncut.edu.tw/var/file/9/1009/attach/40/pta_65271_3490401_17435.pdf",
                },
                {
                    "title": "114 學年度半導體製造實務技術專班學分計畫表",
                    "type": "PDF",
                    "href": "https://oaa.ncut.edu.tw/var/file/9/1009/attach/26/pta_65303_7948568_18887.pdf",
                },
                {
                    "title": "海外青年技術訓練班原始頁面",
                    "type": "原系網",
                    "href": "https://n063.ncut.edu.tw/p/412-1063-8200.php?Lang=zh-tw",
                },
            ],
        },
    ]

    SITE_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
