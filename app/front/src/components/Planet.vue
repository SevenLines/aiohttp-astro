<template>
  <div class="planet" :id="name" :style="style" data-toggle="tooltip" :title="title">
    <div class="icon" :style="iconStyle"></div>
    <div class="degree" :style="degreeStyle">{{(lon_deg % 30).toFixed()}}°</div>
    <div class="reverse" :style="degreeStyle" v-if="reverse">r</div>
    <div class="day" :style="degreeStyle" v-if="day" data-toggle="tooltip" :title="`${day.start} - ${day.end}`">{{day.number}}d</div>
  </div>
</template>


<script>
  export default {
    name: 'planet',
    props: [
      'alt',
      'az',
      'ra',
      'dec',
      'lon',
      'name',
      'width',
      'circle-width',
      'reverse',
      'day'
    ],
    computed: {
      title () {
        return `${this.name} - lon:${this.lon_deg.toFixed(2)}`
      },
      az_deg () {
        return Math.degrees(this.az)
      },
      dec_deg () {
        return Math.degrees(this.dec)
      },
      ra_deg () {
        return Math.degrees(this.ra)
      },
      alt_deg () {
        return Math.degrees(this.alt)
      },
      lon_deg () {
        return Math.degrees(this.lon)
      },
      length () {
        return this.width / 2 - this.circleWidth
      },
      degreeStyle () {
        return {
          transform: `rotate(${this.lon_deg}deg)`,
          fontSize: `${this.circleWidth / 3}px`
        }
      },
      style () {
        return {
          transform: `translate(-50%, -50%) rotate(${-this.lon_deg.toFixed(2)}deg) translate(${this.length}px, 0)`,
          width: `${this.circleWidth}px`,
          height: `${this.circleWidth}px`,
          borderRadius: `${this.circleWidth}px`
        }
      },
      iconStyle () {
        return {
          transform: `translate(-50%, -50%) rotate(${this.lon_deg}deg)`
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
    box-shadow: 0 0 0 2px white;
    /*border: 2px solid white;*/
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

    .degree {
      position: absolute;
      right: -0.75em;
      top: -0.5em;
      background-color: white;
      border-radius: 1.5em;
      padding: 0.3em;
        font-size: 0.75em;
    }

    .day {
      position: absolute;
      left: -0.75em;
      top: -0.5em;
      background-color: #ffba00;
      border-radius: 1.5em;
      padding: 0.3em;
        font-size: 0.75em;
    }

    .reverse {
      position: absolute;
      right: -0.75em;
      bottom: -0.5em;
      padding: 0 0.5em;
      background-color: #ff0053;
      border-radius: 1.5em;
      text-align: center;
      font-size: 0.75em;
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
    background-color: rgba($color, 0.85);
    &:hover {
      background-color: $color;
      color: $fore-color;
    }
  }

  #moon {
    @include planet('☽', #f8f8f8);
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
    @include planet('♆', #f2001f, #000000);
    .icon:before {
      content: '♇';
    }
  }
</style>
