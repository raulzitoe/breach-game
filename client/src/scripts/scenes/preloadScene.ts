import { io, Socket } from "socket.io-client";

export default class PreloadScene extends Phaser.Scene {
  controls

  constructor() {
    super({ key: 'PreloadScene' })
  }
    
  preload() {
    // this.load.image('tiles', 'assets/tileset.png')
    // this.load.tilemapTiledJSON('map', 'assets/hexagonal.json')
    this.load.image('tiles', 'assets/fullTiles.png')
    this.load.tilemapTiledJSON('map', 'assets/tiled_map.json')
  }

  create() {
    const socket = io("http://localhost:8000");
    socket.emit("message", {'message': 'hello world risos'});
    
    var map = this.add.tilemap('map')

    var tileset = map.addTilesetImage('tile5', 'tiles')

    map.createLayer('Tile Layer 1', tileset)
    map.createLayer('Tile Layer 2', tileset)

    var cursors = this.input.keyboard.createCursorKeys()

    this.cameras.main.setZoom(2)
    this.cameras.main.centerOn(0, 0)
    this.add.text(0, 0, 'Hello World', { fontSize: "32px", color: "#000" });

    var controlConfig = {
      camera: this.cameras.main,
      left: cursors.left,
      right: cursors.right,
      up: cursors.up,
      down: cursors.down,
      acceleration: 0.05,
      drag: 0.001,
      maxSpeed: 1.4
    }

    this.controls = new Phaser.Cameras.Controls.SmoothedKeyControl(controlConfig)
  
  
  }

  update(time, delta) {
    this.controls.update(delta)
  }
}

interface ServerToClientEvents {
  noArg: () => void;
  basicEmit: (a: number, b: string, c: Buffer) => void;
  withAck: (d: string, callback: (e: number) => void) => void;
}

interface ClientToServerEvents {
  hello: () => void;
}

interface InterServerEvents {
  ping: () => void;
}

interface SocketData {
  name: string;
  age: number;
}