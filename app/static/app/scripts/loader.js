window.addEventListener("load", function () {
    "use strict";

    var w = window.innerWidth, h = window.innerHeight;
    var bottomx = 0, bottomy = 0, bottomz = 0;
    //renderer
    var renderer = new THREE.WebGLRenderer();
    renderer.setSize(w, h);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.gammaInput = true;
    renderer.gammaOutput = true;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.renderReverseSided = false;
    var view = document.getElementById("view");
    view.appendChild(renderer.domElement);

    var camera = new THREE.PerspectiveCamera(45, w / h, 1, 1000);
    //camera.position.set(100, 100, 200);
    camera.position.set(200, 200, 200);
    var cameraTarget = new THREE.Vector3(0, 0, 0);

    //var controls = new THREE.TrackballControls(camera, view);
    var controls = new THREE.OrbitControls(camera, view);

    controls.rotateSpeed = 0.2;
    controls.zoomSpeed = 1;
    controls.panSpeed = 0.1;
    controls.enableZoom = true;
    controls.enablePan = true;
    controls.enableDamping = true;
    controls.dampingFactor = 0.2;
    controls.keys = [65, 83, 68];
    controls.screenSpacePanning = true;

    var scene = new THREE.Scene();
    scene.add(new THREE.AmbientLight(0x666666));
    scene.background = new THREE.Color(0x262626);

    function addShadowedLight(x, y, z, color, intensity) {
        var directionalLight = new THREE.DirectionalLight(color, intensity);
        directionalLight.position.set(x, y, z);
        scene.add(directionalLight);
        directionalLight.castShadow = true;
        var d = 1;
        directionalLight.shadow.camera.left = -d;
        directionalLight.shadow.camera.right = d;
        directionalLight.shadow.camera.top = d;
        directionalLight.shadow.camera.bottom = -d;
        directionalLight.shadow.camera.near = 1;
        directionalLight.shadow.camera.far = 4;
        directionalLight.shadow.mapSize.width = 1024;
        directionalLight.shadow.mapSize.height = 1024;
        directionalLight.shadow.bias = -0.005;
    }

    //scene.add(new THREE.HemisphereLight(0xe6e6e6, 0x404040));
    addShadowedLight(1, 1, 1, 0xffffff, 1.35);
    addShadowedLight(0.5, 1, -1, 0xffffff, 1);

    var mat = new THREE.MeshPhongMaterial({
        color: 0xff8000, specular: 0x111111, shininess: 30
    });
    var obj = new THREE.Mesh(new THREE.Geometry(), mat);
    obj.position.set(0, -0.25, 0.6);
    obj.rotation.set(0, -Math.PI / 2, 0);

    obj.castShadow = true;
    obj.receiveShadow = true;
    scene.add(obj);

    //grid
    var mygrid = new THREE.GridHelper(200, 20, 0xff8000, 0x3B3B3B);
    mygrid.position.y = 0;
    mygrid.position.x = 0;
    mygrid.position.z = 0;
    scene.add(mygrid);

    var loop = function loop() {
        requestAnimationFrame(loop);
        //obj.rotation.z += 0.05;
        controls.update();
        renderer.clear();
        renderer.render(scene, camera);
    };
    loop();

    // file load
    var openFile = function (file) {
        var reader = new FileReader();
        reader.addEventListener("load", function (ev) {
            var buffer = ev.target.result;
            var geom = loadStl(buffer);

            scene.remove(obj);
            scene.remove(mygrid);

            obj = new THREE.Mesh(geom, mat);

            obj.rotation.set(-Math.PI / 2, 0, 0);
            var box = new THREE.Box3().setFromObject(obj);
            //box.getCenter(obj.position); // this re-sets the mesh position
            obj.position.x = - (box.max.x - (box.max.x - box.min.x)/2); //place center of bounding box at coordinate center
            obj.position.y = - box.min.y; //place object above y=0 plane.
            obj.position.z = - (box.max.z - (box.max.z - box.min.z)/2);
            scene.add(obj);

            mygrid.position.x = 0;
            mygrid.position.y = 0;
            mygrid.position.z = 0;

            scene.add(mygrid);

        }, false);
        reader.readAsArrayBuffer(file);
    };

    // file input button
    var input = parent.document.getElementById("stlpath");
    var path = input.innerHTML;
    var blob = null;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", path);
    xhr.responseType = "blob";
    xhr.onload = function (e) {
        blob = xhr.response;
        openFile(blob);
    };
    xhr.send();
    
    // dnd
    view.addEventListener("dragover", function (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        ev.dataTransfer.dropEffect = "copy";
    }, false);

    view.addEventListener("drop", function (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        var file = ev.dataTransfer.files[0];
        openFile(file);
    }, false);
}, false);