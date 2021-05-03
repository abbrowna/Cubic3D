import * as THREE from './three.module.js';
import { STLLoader } from './STLLoader.js';

var container;
var camera, cameraTarget, scene, renderer, controls, mesh;
var path, color, hexcolor;

init();

animate();


function init() {

    container = document.createElement( 'div' );
    document.body.appendChild(container);

    camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(500, 500, 500);

    cameraTarget = new THREE.Vector3(0, 0, 0);

    scene = new THREE.Scene();
    scene.add(new THREE.AmbientLight(0x666666));
    scene.background = new THREE.Color(0x262626);

    //Global grid on ground
    var grid = new THREE.GridHelper(300, 20, 0xff8000, 0x3B3B3B);
    grid.position.y = 0;
    grid.position.x = 0;
    grid.position.z = 0;
    scene.add(grid);

    //Load/reload the mesh object and grid
    path = parent.document.getElementById("stlpath").innerHTML;
    color = parent.document.getElementById("stlcolor").innerHTML;
    hexcolor = colorNametoHex(color);
    console.log(color);
    console.log(hexcolor);
    var loader = new STLLoader();
    loader.load(path, function (geometry) {
        var material = new THREE.MeshPhongMaterial({
            color: hexcolor,
            specular: 0x111111,
            shininess: 30
        });

        if (color.toLowerCase() === "clear"){
            material.opacity = 0.9;
            material.transparent = true;
            material.side = THREE.DoubleSide;
        }
        console.log(material);
        mesh = new THREE.Mesh(geometry, material);

        mesh.rotation.set(-Math.PI / 2, 0, 0);

        var box = new THREE.Box3().setFromObject(mesh);
        
        mesh.position.x = - (box.max.x - (box.max.x - box.min.x) / 2); //place center of bounding box at coordinate center
        mesh.position.y = - box.min.y; //place object above y=0 plane.
        mesh.position.z = - (box.max.z - (box.max.z - box.min.z) / 2);

        mesh.castShadow = true;
        mesh.receiveShadow = true;

        scene.add( mesh );

    });
    addShadowedLight(1, 1, 1, 0xffffff, 1.35);
    addShadowedLight(0.5, 1, -1, 0xffffff, 1);

    //renderer
    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.outputEncoding = THREE.sRGBEncoding;

    renderer.shadowMap.enabled = true;
    
    container.appendChild(renderer.domElement);
    window.addEventListener('resize', onWindowResize, false);


}


function addShadowedLight(x, y, z, color, intensity) {

    var directionalLight = new THREE.DirectionalLight(color, intensity);
    directionalLight.position.set(x, y, z);
    scene.add(directionalLight);

    directionalLight.castShadow = true;

    var d = 1;
    directionalLight.shadow.camera.left = - d;
    directionalLight.shadow.camera.right = d;
    directionalLight.shadow.camera.top = d;
    directionalLight.shadow.camera.bottom = - d;

    directionalLight.shadow.camera.near = 1;
    directionalLight.shadow.camera.far = 4;

    directionalLight.shadow.bias = - 0.002;

}

function onWindowResize() {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);

}

//function render() {

//    camera.lookAt(cameraTarget);
//    renderer.render(scene, camera);
//}

function render() {
    var timer = Date.now() * 0.0005;

    camera.position.x = Math.cos(timer) * 400;
    camera.position.z = Math.sin(timer) * 400;
    camera.position.y = 100;

    camera.lookAt(cameraTarget);

    renderer.render(scene, camera);
}

function animate() {

    requestAnimationFrame(animate);
    render();

}

function colorNametoHex(color) {
    var colors =
    {
        "black": 0x000000,
        "white": 0xffffff,
        "blue": 0x00bfff,
        "grey": 0x808080,
        "gray": 0x808080,
        "green": 0x7cfc00,
        "clear": 0xeeeeee,
        "red": 0xff0000
    };
    if (typeof colors[color.toLowerCase()] !== 'undefined')
        return colors[color.toLowerCase()];

    return 0xeeeeee;
}

