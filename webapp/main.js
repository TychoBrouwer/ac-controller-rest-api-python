class ACcontroller {
  serverAddress = 'https://accontroller.tbrouwer.com/'
  clientID = 'CLIENT IDENTIFIER'
  deviceID = 'DEVICE IDENTIFIER'

  acState;
  toUpdate = {};

  constructor() {
    this.init();
  }

  async init() {
    await this.fetchState();
  }

  async fetchState() {
    const request = await fetch(this.serverAddress + 'get-device?clientID=' + this.clientID + '&deviceID=' + this.deviceID);

    const response = await request.json();
    if (response.code === 200) {
      console.log(response.settings);
      this.acState = response.settings;

      document.getElementById('protocol').innerText = 'Protocol: ' + this.acState.protocol;

      Object.entries(this.acState).forEach(([key, value]) => {
        this.setValue(key, value, false);
      });
    }

    return response;
  }

  async sendState() {
    if (Object.keys(this.toUpdate).length === 0) return;

    console.log(this.toUpdate);

    const operation = {
      op: "update-settings",
      settings: this.toUpdate
    }

    const request = await fetch(
      this.serverAddress + 'update-device' +
      '?clientID=' + this.clientID +
      '&deviceID=' + this.deviceID +
      '&operation=' + JSON.stringify(operation)
    );

    const response = await request.json();

    if (response.code === 200) {
      Object.entries(this.toUpdate).forEach(([key, value]) => {
        this.acState[key] = value;

        this.setValue(key, value, false);
        this.setValue(key, undefined, true);
      });

      this.toUpdate = {};
    }

    return response;
  }

  setValue(key, value, update) {
    let element;
    if (update) {
      element = document.getElementById(key)?.getElementsByClassName('value-update')[0];
    } else {
      element = document.getElementById(key)?.getElementsByClassName('value')[0];
    }

    if (!element) {
      return;
    }

    if (value == undefined) {
      element.innerHTML = '';
      return;
    }

    const classes = element.classList;

    if (classes.contains('integer')) {
      element.innerHTML = parseInt(value);
    } else if (classes.contains('boolean')) {
      element.innerHTML = value === "1" ? "On" : "Off";
    } else {
      element.innerHTML = value;
    }
  }

  changePower() {
    this.toUpdate.power = this.acState.power === "0" ? "1" : "0";

    this.setValue('power', this.toUpdate.power, true);
  };

  changeMode() {

  };

  changeTemp(increase) {
    const temp = this.toUpdate.degrees ? this.toUpdate.degrees : this.acState.degrees;
    this.toUpdate.degrees = String(parseInt(temp) + (increase ? 1 : -1));

    this.setValue('degrees', this.toUpdate.degrees, true);
  };
}

ACcontroller = new ACcontroller();