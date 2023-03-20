class ACcontroller {
  serverAddress = 'https://accontroller.tbrouwer.com/'
  clientID = 'CLIENT IDENTIFIER'
  deviceID = 'DEVICE IDENTIFIER'

  constructor() {
    this.init();
  }

  async init() {
    const acState = await fetch(this.serverAddress + 'get-device?clientID=' + this.clientID + '&deviceID=' + this.deviceID, {
      method: 'GET',
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
        'mode': 'no-cors'
      }
    });
    console.log(acState);
  }

  changePower() {

  };

  changeMode() {

  };

  tempUp() {

  };

  tempDown() {

  };
}

ACcontroller = new ACcontroller();