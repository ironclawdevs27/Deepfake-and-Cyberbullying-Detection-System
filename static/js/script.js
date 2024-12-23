body {
    height: 100%;
    margin: 0;
    padding: 0;
    color: black;
}
/* .bg {
    background-image: url("/static/images/background1.png");
    height: 90vh;
    width: 100vw;
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-position: center;
    background-repeat: repeat;
    background-size: cover;
    margin-top: 0;
    padding-top: 0;
} */
.bg {
    position: relative;
    height: 90vh;
    width: 100vw;
    margin-top: 0;
    padding-top: 0;
    background-color: rgba(0, 0, 0, 0.5);
}
.bg-video {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    object-fit: cover;
    z-index: -1;
}
.container {
    position: relative;
    z-index: 1;
}
#video-upload-section {
    display: none;
}
section {
    padding-top: 60px;
}
.container {
    margin-top: 0;
    padding-top: 0;
}
#video-upload-section {
    display: none;
}
#get-started-btn {
    padding: 15px 30px;
    font-size: 2.5em;
    font-weight: 500;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 15px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    transition: background 0.3s ease, backdrop-filter 0.3s ease;
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    position: absolute;
    top: 290px;
    left: 50%;
    transform: translateX(-50%);
}
#get-started-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
    cursor: pointer;
}
.glassmorphism {
    background: rgba(255, 255, 255, 0.1);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    transition: backdrop-filter 0.3s ease, -webkit-backdrop-filter 0.3s ease, background 0.3s ease;
}
.glassmorphism:hover {
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.2);
}
.glassmorphism-logo {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 10px;
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    display: inline-block;
    position: absolute;
    top: 40px;
    left: 50%;
    transform: translateX(-50%);
}
.glassmorphism-logo:hover {
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.2);
}
.width-300 {
    width: 300px;
    margin: auto;
    padding: 20px;
    box-shadow: 0 0px 9px 2px #ccc;
    position: absolute;
    top: 150px;
    left: 50%;
    transform: translateX(-50%);
}
.width-300,
.width-400,
.width-500 {
    background: rgba(255, 255, 255, 0.1);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    transition: backdrop-filter 0.3s ease, -webkit-backdrop-filter 0.3s ease, background 0.3s ease;
    position: absolute;
    top: 140px;
    left: 50%;
    transform: translateX(-50%);
}
#preprocessed_images,
#faces_images, .result {
    background: rgba(255, 255, 255, 0.1);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    transition: backdrop-filter 0.3s ease, -webkit-backdrop-filter 0.3s ease, background 0.3s ease;
}
.width-300:hover,
.width-400:hover,
.width-500:hover,
#preprocessed_images:hover,
#faces_images:hover, .result:hover {
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.2);
}
.width-400 {
    width: 400px;
    margin: auto;
    padding: 20px;
    margin-top: 80px;
    margin-bottom: 150px;
    box-shadow: 0 0px 9px 2px #ccc;
}
.width-500 {
    width: 500px;
    margin: auto;
    padding: 20px;
    box-shadow: 0 0px 9px 2px #ccc;
}
#videos {
    display: none;
}
canvas {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
}
#preprocessed_images {
    width: auto;
    height: 250px;
    padding: 20px;
    overflow-x: scroll;
    overflow-y: hidden;
    box-shadow: 0 0px 9px 2px #ccc;
    position: relative;
    margin-top: 120px;
}
.preprocess {
    padding-right: 20px;
    padding-bottom: 50px;
}
#faces_images {
    white-space: nowrap;
    width: auto;
    height: 150px;
    padding: 20px;
    overflow-x: scroll;
    overflow-y: hidden;
    box-shadow: 0 0px 9px 2px #ccc;
    position: relative;
    margin-top: 20px;
}

.faces {
    padding-right: 20px;
    padding-bottom: 50px;
}

.result {
    box-shadow: 0 0px 9px 2px #ccc;
    position: relative;
    text-align: center;
    margin-top: 20px;
}

.result h3 {
    margin-top: 25px;
}

.result video {
    display: block;
    margin: 10px auto;
}

.result h4, .result img {
    margin-top: 10px;
}
