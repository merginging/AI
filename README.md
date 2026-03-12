# AI와 다양한 협업툴을 연결해 분산된 정보를 통합하여 제공하는 협업 플러그인 README

<img width="1221" height="682" alt="image" src="https://github.com/user-attachments/assets/1e910be4-8c34-4a7a-a1e5-d9ddd325201c" />


-   배포 URL : https://merging-fe.vercel.app/
-   Test ID : test@gmail.com
-   Test PW : test1234

<br>

## 프로젝트 소개

브랜치파이(Branchify)는 AI와 다양한 협업 툴을 연결해 분산된 정보를 통합 제공하는 협업 플러그인 서비스입니다. 이 서비스는 AI-Agent가 여러 협업 툴에 흩어진 업무 데이터를 통합 관리하고 자동화하며, 문맥을 분석하여 관련 자료를 추천하는 AI 기반 자동화 기능을 제공합니다. 또한 사용자가 필요에 따라 AI-Agent와 협업 툴을 조합해 맞춤형 플러그인 형태로 확장할 수 있습니다.

<br>

## 팀원 구성

<div align="center">

|                                                         **권소현**                                                          |                                                                 **남윤혁**                                                                  |                                                         **박우찬**                                                          |                                                              **유주영**                                                               |
| :-------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------: |
| [<img src="https://avatars.githubusercontent.com/hyuke81" height=150 width=150> <br/> @hyuke81](https://github.com/hyuke81) | [<img src="https://avatars.githubusercontent.com/namyoonhyeok" height=150 width=150> <br/> @namyoonhyeok](https://github.com/namyoonhyeok) | [<img src="https://avatars.githubusercontent.com/pwc2002" height=150 width=150> <br/> @pwc2002](https://github.com/pwc2002) | [<img src="https://avatars.githubusercontent.com/Juyounge-e" height=150 width=150> <br/> @Juyounge-e](https://github.com/Juyounge-e) |

</div>

<br>

## 1. 개발 환경

-   Front : React, Vite, emotion.js, axios
-   Back-end :
-   버전 및 이슈관리 : Github, Github Issues, Github Action
-   협업 툴 : Notion, Discord
    <br>

## 2. 채택한 개발 기술과 브랜치 전략

### React, emotion.js

-   React

    -   컴포넌트 기반 아키텍처를 활용해 UI를 구조화했습니다.
    -   이를 통해 코드의 유지보수성과 재사용성을 높여 개발 효율을 극대화했습니다.

    -   특히 유저 배너, 상단/하단 배너 등 반복되는 요소를 컴포넌트화하여 리소스 낭비를 줄였습니다.

-   emtion.js

    -   CSS-in-JS 라이브러리로, 컴포넌트 내에서 스타일을 직접 작성했습니다.

    -   props를 이용한 조건부 스타일링 덕분에 상황에 따라 유동적인 UI를 구현하기가 용이했습니다.

    -   자동으로 고유한 클래스 이름이 부여되므로, 별도의 네이밍 컨벤션을 정하는 수고를 덜 수 있었습니다.

### eslint, prettier

-   eslint
    -   코드의 잠재적인 버그나 문제점을 사전에 발견하고, 코딩 스타일을 통일하는 데 사용했습니다.
    -   Airbnb의 엄격한 코딩 컨벤션을 적용하여 팀 전체의 코드 품질을 높이는 데 집중했습니다.
-   prettier
    -   코드 포맷팅을 자동으로 처리하여 코드의 일관성을 유지했습니다.
    -   개발자가 일일이 코드 스타일을 신경 쓸 필요 없이 빠르게 개발에 집중할 수 있도록 도와주었습니다.

<br>

## 3. 프로젝트 구조

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml
├── node_modules/
├── src/
│   ├── api/
│   ├── assets/
│   │   ├── fonts/
│   │   ├── icons/
│   │   └── images/
│   ├── components/
│   │   ├── BotAi/
│   │   │   ├── modal/
│   │   │   ├── BotStep1.jsx
│   │   │   ├── BotStep1.styles.js
│   │   │   ├── BotStep2.jsx
│   │   │   ├── BotStep2.styles.js
│   │   │   ├── BotStep3.jsx
│   │   │   └── BotStep3.styles.js
│   │   ├── Box/
│   │   ├── Footer/
│   │   ├── Header/
│   │   ├── BotLayout.jsx
│   │   ├── Layout.jsx
│   │   └── Sidebar.jsx
│   ├── pages/
│   │   ├── Bot/
│   │   ├── Home/
│   │   │   ├── BetatestBanner/
│   │   │   ├── JoinForm/
│   │   │   ├── Main/
│   │   │   │   ├── Feature2.jsx
│   │   │   │   ├── Fy.jsx
│   │   │   │   ├── Home.jsx
│   │   │   │   ├── Intro.jsx
│   │   │   │   └── Prepare.jsx
│   │   │   └── Home.jsx
│   │   ├── Login/
│   │   ├── Price/
│   │   └── Signup/
│   ├── stores/
│   ├── App.jsx
│   ├── index.css
│   ├── main.jsx
│   └── routes.jsx
├── .gitignore
├── .prettierrc
├── build.sh
└── eslint.config.js

```

<br>

## 4. 개발 기간

### 개발 기간

-   전체 개발 기간 : 2025-01-04 ~ 2025-02-28

<br>

### 5. 사용자 기능

-   AI 기반 검색 기능

    -   문서, 대화 맥락을 기반으로 AI가 필요한 정보를 검색하여 제공합니다.

-   대화 요약 및 정리 기능

    -   채팅형 서비스(Slack, Discord 등)의 대화 내용을 요약하고, 회의 내용, 주요 결정사항, 액션 아이템을 자동으로 정리해 줍니다.

-   AI 기반 업무 자동화

    -   일정 알림, 태스크 업데이트와 같은 반복적인 업무를 AI가 자동으로 처리하여 사용자의 업무 효율을 높여줍니다.

-   AI 챗봇 기능

    -   메신저의 챗봇에 질문하면, 여러 협업 툴에서 관련된 정보를 자동으로 찾아 답변해 줍니다.

-   통합된 업무 환경 제공

    -   Notion, Jira, PDF 문서 등 다양한 협업 툴과 연동하여 채팅형 SaaS에서 모든 업무를 한 곳에서 관리할 수 있습니다.

-   간단한 설정 및 직관적인 UI - 경쟁 서비스에 비해 설정이 간단하고, 기존 협업 툴 인터페이스에서 바로 도입할 수 있어 누구나 쉽게 사용할 수 있습니다.
    <br>
