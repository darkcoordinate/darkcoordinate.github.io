// Daniel Shiffman
// http://codingtra.in
// http://patreon.com/codingtrain

// Video: https://youtu.be/H81Tdrmz2LA

// Original GIF: https://beesandbombs.tumblr.com/post/149654056864/cube-wave

let angle = 0;
let w = 24;
let ma;
let maxD;

function setup() {
	createCanvas(400, 400, WEBGL);
	ma = atan(cos(QUARTER_PI));
	maxD = dist(0, 0, 200, 200);
}


let gyroscope = new Gyroscope({ frequency: 60 });

gyroscope.addEventListener('reading', e => {
	document.getElementById("gx").innerHTML = gyroscope.x;
	document.getElementById("gy").innerHTML = gyroscope.y;
	document.getElementById("gz").innerHTML = gyroscope.z;
	console.log("Angular velocity along the X-axis " + gyroscope.x);
	console.log("Angular velocity along the Y-axis " + gyroscope.y);
	console.log("Angular velocity along the Z-axis " + gyroscope.z);
});
gyroscope.start();

function draw() {
	background(255);
	ortho(-400, 400, 400, -400, 0, 1000);
	rotateX(-ma);
	rotateY(-QUARTER_PI);
	//normalMaterial()
	//sphere(40);
	for (let z = 0; z < height; z += w) {
		for (let x = 0; x < width; x += w) {
			push();
			let d = dist(x, z, width / 2, height / 2);
			let offset = map(d, 0, maxD, -PI, PI);
			let a = angle + offset;
			let h = floor(map(sin(a), -1, 1, 100, 300));
			translate(x - width / 2, 0, z - height / 2);
			normalMaterial();
			box(w, h, w);
			//rect(x - width / 2 + w / 2, 0, w - 2, h);
			pop();
		}
	}

	angle -= 0.1;
}