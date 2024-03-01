<!-- Back to Top Link-->
<a name="readme-top"></a>


<br />
<div align="center">
  <h1 align="center">Tugas Besar 1 IF2211 Strategi Algoritma
</h1>

  <p align="center">
    <h3>Diamonds bot</h3>
    <h4>  Pemanfaatan Algoritma Greedy dalam pembuatan bot </h4>
    <br/>
    <!-- IMAGE OR LOGO -->
    <!-- <img src="" alt="Project Logo // Team Picture // etc">
    <br/>
    <br/> -->
    <a href="https://github.com/NoHaitch/Tubes1_SanssKuy/issues">Report Bug</a>
    ·
    <a href="https://github.com/NoHaitch/Tubes1_SanssKuy/issues">Request Feature</a>
<br>
<br>

[![MIT License][license-shield]][license-url]

  </p>
</div>

<!-- CONTRIBUTOR -->
<div align="center" id="contributor">
  <strong>
    <h3>Made By:</h3>
    <h3>Team Sanss Kuy</h3>
    <!-- OPTIONAL TABLE FOR MULTIPLE PEOPLE -->
    <table align="center">
      <tr>
        <td>NIM</td>
        <td>Name</td>
      </tr>
      </tr>
      <tr>
        <td>13522091</td>
        <td>Raden Francisco Trianto Bratadiningrat</td>
      </tr>
      <tr>
        <td>13522105</td>
        <td>Fabian Radenta Bangun</td>
      </tr>
      </tr>
      <tr>
        <td>13522132</td>
        <td>Hafizh Hananta Akbari</td>
      </tr>
    </table>
  </strong>
  <br>
  <h3> NOTE: Our team Main Bot is BotGreedyPath</h3>
  <br>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#instruction">Instruction</a></li>
        <li>
        <details>
          <summary><a href="#features-bots">Features</a></summary>
          <ol>
            <li><a href="#1-greedy-by-path-main-bot">Greedy by Path (MAIN BOT)</a></li>
            <li><a href="#2-greedy-by-points">Greedy By Points</a></li>
            <li><a href="#3-chase-enemy">Chase Enemy</a></li>
            <li><a href="#4-chase-enemy">Random Logic</a></li>
          <ol>
        </details>
        </li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## External Links
*some links may be oudated or removed*

- [Game Engine](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)
- [Bot Starter Pack](https://github.com/haziqam/tubes1-IF2211-bot-starter-pack/releases/tag/v1.0.1)
- [Spesifikasi](https://docs.google.com/document/d/13cbmMVXviyu8eKQ6heqgDzt4JNNMeAZO/edit)
- [Teams](https://docs.google.com/spreadsheets/d/1ZILn6qF6UQxNtX9gTAW3OLUATywvMxiH6ZWjcOHQIMk/edit#gid=0)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ABOUT THE PROJECT -->
## About The Project

General Explanation about the project, Why you made this, What does it do exactly.  

<!-- OPTIONAL LINK OR REFERENCE -->
<!-- <p align="center">
You can explore more on this link ... 
<br>
<a href="https://example.com"> <Strong>THIS LINK</Strong>
</a>
</p> -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Project dependencies  

* Python
  ```sh
  # in Windows
  https://www.python.org/downloads/

  # in Linux
  sudo apt install python3
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

For installing and running the game engine please see [Get Started with Diamonds](https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit)  
This are the steps to run and use the bots.   

1. Clone the repo
   ```sh
   git clone https://github.com/NoHaitch/Tubes1_SanssKuy
   ```
2. Change directory
   ```sh
   cd src/bot
   ```
3. Run a Bot
   ```sh
   # format
   python main.py --logic <BotClassName> --email=<Email> --name=<BotName>  --password=<Password> --team etimo

   # example
   python main.py --logic BotGreedyPath --email=test6@email.com --name=main --password=123456 --team etimo
   ```

  - `BotClassName` : class name of the bot you want, currently option are Random, BotGreedyPoints, BotGreedyPath, and BotChase  
  - `Email` : email bust be in valid format (ex: your_email@example.com), each bot must have a unique email  
  - `BotName` : bot name must be unique and limited to 10 characters  
    &nbsp;
   
4. Run multiple Bots
   ```sh
   # in Windows
   ./run-bots.bat

   # in Linux
   ./run-bots.sh
   ```


For further information please refer to [Get Started with Diamonds](https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit) 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Bots -->
## Features (Bots)

### 1. Greedy by Path (MAIN BOT)
### 2. Greedy By Points
### 3. Chase Enemy
### 4. Random Logic

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

If you want to contribute or further develop the program, please fork this repository using the branch feature.  
Pull Request is **permited and warmly welcomed**
<!-- In bahasa Indonesia: Jika Anda ingin berkontribusi atau melanjutkan perkembangan program, silahkan fork repository ini dan gunakan branch fitur.  

Permintaan Pull __sangat diperbolehkan dan diterima dengan hangat__. -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## Licensing

The code in this project is licensed under MIT license.  
<!-- Add other targeted langguage: Code dalam projek ini berada di bawah lisensi MIT. -->


<!-- SPECIAL THANKS AND/OR CREDITS -->
<!-- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) by othneildrew -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<br>
<h3 align="center"> THANK YOU! </h3>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-url]: https://github.com/NoHaitch/Tubes1_SanssKuy/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/NoHaitch/Tubes1_SanssKuy/blob/main/LICENSE
