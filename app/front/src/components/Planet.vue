<template>
  <div class="planet" :id="name" :style="style" data-toggle="tooltip" :title="title"
  ></div>
</template>


<script>
  export default {
    name: 'planet',
    props: ['alt', 'az', 'ra', 'dec', 'name', 'width', 'circle-width'],
    computed: {
      title () {
        return `${this.name} - alt:${this.alt_deg.toFixed(2)} ra:${this.ra_deg.toFixed(2)} az:${this.az_deg.toFixed(2)}`
      },
      az_deg () {
        return this.az * (180 / Math.PI)
      },
      dec_deg () {
        return this.dec * (180 / Math.PI)
      },
      ra_deg () {
        return this.ra * (180 / Math.PI)
      },
      alt_deg () {
        return this.alt * (180 / Math.PI)
      },
      length () {
        return this.width / 2
      },
      style () {
        return {
          transform: `translate(-50%, -50%) rotate(${this.ra_deg}deg) translate(${this.length}px, 0)`,
          width: `${this.circleWidth}px`,
          height: `${this.circleWidth}px`,
          borderRadius: `${this.circleWidth}px`
        }
      }
    }
  }
</script>

<style lang="scss">
  @mixin size($width) {
    height: $width;
    width: $width;
    border-radius: $width;
  }

  .planet {
    position: absolute;
    left: 50%;
    top: 50%;

    display: block;

    background-color: white;
    border: 1px solid silver;

    -webkit-transition: all 0.1s;
    -moz-transition: all 0.1s;
    -ms-transition: all 0.1s;
    -o-transition: all 0.1s;
    transition: all 0.1s;
    color: white;

  }

  #center {
    position: absolute;
    left: 50%;
    top: 50%;
    display: block;
    height: 3px;
    width: 3px;
    border-radius: 3px;
    border: 1px solid black;
  }

  #moon {
    background-color: #ffffff;

  }

  #sun {
    background-color: #ff0b00;
  }

  #mercury {
    background-color: #a9ff00;
  }

  #venus {
    background-color: #00a7ff;
  }

  #mars {
    background-color: #ffdd00;
  }

  #jupiter {
    background-color: #23f3ff;
  }

  #saturn {
    background-color: #b10fff;
  }

  #uranus {
    background-color: #ffffff;
  }

  #neptune {
    background-color: #ffffff;
  }

  #pluto {
    background-color: #ffffff;
  }
</style>
