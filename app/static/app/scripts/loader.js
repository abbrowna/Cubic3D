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
    camera.position.set(100, 100, 200);
    var cameraTarget = new THREE.Vector3(0, 0, 0);

    var controls = new THREE.TrackballControls(camera, view);

    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;
    controls.noZoom = false;
    controls.noPan = false;
    controls.staticMoving = true;
    controls.dynamicDampingFactor = 0.3;
    controls.keys = [65, 83, 68];

    var scene = new THREE.Scene();
    scene.add(new THREE.AmbientLight(0x666666));
    scene.background = new THREE.Color(0x333333);

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
    var mygrid = new THREE.GridHelper(200, 20, 0xff8000, 0x808080);
    mygrid.position.y = 0.5;
    mygrid.position.x = 0;
    mygrid.position.z = 0;
    scene.add(mygrid);

    //ground
    //var plane = new THREE.Mesh(
    //    new THREE.PlaneBufferGeometry(200, 200),
    //    new THREE.MeshPhongMaterial({ color: 0x999999, specular: 0x101010 })
    //);
    //plane.rotation.x = -Math.PI / 2;
    //plane.position.x = 0;
    //plane.position.y = 0.5;
    //plane.position.z = 0;
    //scene.add(plane);
    //plane.receiveShadow = true;

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

            var box = new THREE.Box3().setFromObject(obj);
            box.center(obj.position); // this re-sets the mesh position
            obj.position.multiplyScalar(- 1);
            scene.add(obj);

            geom.computeBoundingBox();
            //mygrid.position.x = geom.boundingBox.min.x;
            mygrid.position.y = 0-((geom.boundingBox.max.y-geom.boundingBox.min.y)/2);
            //mygrid.position.z = geom.boundingBox.min.z;
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
    xhr.onload = function (e)
    {
        blob = xhr.response;
        openFile(blob);
    }
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