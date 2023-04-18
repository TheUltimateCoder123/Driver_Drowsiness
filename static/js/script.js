// // Get access to the video element
// const video = document.getElementById('video');

// // Get access to the canvas element and its context
// const canvas = document.getElementById('canvas');
// const context = canvas.getContext('2d');

// // Set the dimensions of the canvas to match the video element
// canvas.width = video.width;
// canvas.height = video.height;

// // Set up the face and eye detection classifiers
// const faceCascade = new cv.CascadeClassifier();
// const eyeCascade = new cv.CascadeClassifier();

// faceCascade.load('haarcascade_frontalface_default.xml');
// eyeCascade.load('haarcascade_eye.xml');

// // Start the video stream and start processing the frames
// navigator.mediaDevices.getUserMedia({ video: true })
// .then(stream => {
//     video.srcObject = stream;
//     video.play();
// })
// .catch(err => {
//     console.error('Unable to access the camera:', err);
// });

// // Process each frame of the video stream
// function processVideo() {
//     // Capture a frame from the video stream and draw it onto the canvas
//     context.drawImage(video, 0, 0, canvas.width, canvas.height);

//     // Convert the canvas image to grayscale and detect faces
//     const img = cv.imread(canvas);
//     const gray = new cv.Mat();
//     cv.cvtColor(img, gray, cv.COLOR_RGBA2GRAY);
//     const faces = new cv.RectVector();
//     faceCascade.detectMultiScale(gray, faces, 1.1, 3);

//     // Loop through each detected face
//     for (let i = 0; i < faces.size(); i++) {
//         const face = faces.get(i);
//         const faceColor = new cv.Scalar(255, 0, 0); // blue

//         // Draw a rectangle around the face
//         cv.rectangle(img, face, faceColor, 2);

//         // Detect eyes within the face region
//         const roiGray = gray.roi(face);
//         const eyes = new cv.RectVector();
//         eyeCascade.detectMultiScale(roiGray, eyes, 1.1, 1);

//         // Loop through each detected eye
//         for (let j = 0; j < eyes.size(); j++) {
//             const eye = eyes.get(j);
//             const eyeColor = new cv.Scalar(0, 255, 0); // green

//             // Draw a rectangle around the eye
//             cv.rectangle(img, new cv.Point(face.x + eye.x, face.y + eye.y), new cv.Point(face.x + eye.x + eye.width, face.y + eye.y + eye.height), eyeColor, 2);
//         }
//     }

//     // Display the processed image on the canvas
//     cv.imshow(canvas, img);

//     // Call the processVideo function again to process the next frame
//     setTimeout(processVideo, 10);
// }

// // Start processing the video stream
// processVideo();
