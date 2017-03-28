<template>
  <div class="planet" :id="name" :style="style" data-toggle="tooltip" :title="title">
    <div class="icon" :style="iconStyle"></div>
  </div>
</template>


<script>
  export default {
    name: 'planet',
    props: ['alt', 'az', 'ra', 'dec', 'lon', 'name', 'width', 'circle-width'],
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
      lon_deg () {
        return this.lon * (180 / Math.PI)
      },
      length () {
        return this.width / 2
      },
      style () {
        return {
          transform: `translate(-50%, -50%) rotate(${this.lon_deg}deg) translate(${this.length}px, 0)`,
          width: `${this.circleWidth}px`,
          height: `${this.circleWidth}px`,
          borderRadius: `${this.circleWidth}px`
        }
      },
      iconStyle () {
        return {
          transform: `translate(-50%, -50%) rotate(${-this.lon_deg}deg)`
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
    cursor: pointer;
    position: absolute;
    left: 50%;
    top: 50%;

    display: block;

    background-color: rgba(255, 255, 255, 0.5);
    box-shadow: 0 0 2px silver;
    font-weight: bold;

    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    -ms-transition: all 0.3s;
    -o-transition: all 0.3s;
    transition: all 0.3s;
    color: black;

    .icon {
      font-size: 1.25em;
      position: absolute;
      left: 50%;
      top: 50%;
    }

    &:hover {
      z-index: 100;
    }

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

  @mixin planet($icon, $color, $fore-color: black) {
    .icon:before {
      content: $icon;
    }
    background-color: rgba($color, 0.25);
    &:hover {
      background-color: $color;
      color: $fore-color;
    }
  }

  #moon {
    @include planet('☽', silver);
  }

  #sun {
    @include planet('☉', #ffc500, red);
  }

  #mercury {
    @include planet('☿', #d0ff00, #5a7800);
  }

  #venus {
    @include planet('♀', #20e7ff, #a9006c);
  }

  #mars {
    @include planet('♂', #ff5b5a, #000000);
  }

  #jupiter {
    @include planet('♃', #ff8940, #ad3d00);
  }

  #saturn {
    @include planet('♄', #be7cf9, #41265d);
  }

  #uranus {
    @include planet('♅', #7df9ee, #38535d);
  }

  #neptune {
    @include planet('♆', #5dff5d, #0e5d09);
  }

  #pluto {
    @include planet('♆', #7c0a00, #ffecf3);
    .icon:before {
      content: '♇';
    }
  }
</style>
