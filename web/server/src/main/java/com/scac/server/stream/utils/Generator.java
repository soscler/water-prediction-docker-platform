package com.scac.server.stream.utils;

import lombok.Data;
import org.springframework.context.annotation.Scope;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;


@Component
@Scope(value = "singleton")
@Data
public class Generator {

    /**
     * Wind direction (in degrees) on average over the last 10 minutes of the past hour
     * (360 = north, 90 = east, 180 = south, 270 = west, 0 = windless 990 = changeable.
     * See http://www.knmi.nl/ knowledge and data center / background / climatic brochures and books
     * */
    private double DD ;

    /**
     * Hourly average wind speed (in 0.1 m / s).
     * */
    private double FH;

    /**
     * Wind speed (in 0.1 m / s) on average over the last 10 minutes of the past hour
     * */
    private double FF;

    /***
     * Highest wind gust (in 0.1 m / s) over the last hour section
     */
    private double FX;

    /**
     * Temperature (in 0.1 degrees Celsius) at 1.50 m height during the observation
     * */
    private double T;

    /**
     * 	Minimum temperature (in 0.1 degrees Celsius) at a height of 10 cm in the last 6 hours
     * */
    private double T10N;

    /**
     * Dew point temperature (in 0.1 degrees Celsius) at 1.50 m altitude during the observation
     * */
    private double TD;

    /**
     * Duration of sunshine (in 0.1 hours) per hour, calculated from global radiation (-1 for <0.05 hours)
     * */
    private double SQ;

    /**
     * Global radiation (in J / cm2) per hour section
     * */
    private double Q;

    /**
     * 	Duration of the precipitation (in 0.1 hours) per hour section
     * */
    private double DR;

    /**
     * Hourly amount of the precipitation (in 0.1 mm) (-1 for <0.05 mm)
     * */
    private double RH;

    /**
     * 	Air pressure (in 0.1 hPa) reduced to sea level during observation
     * */
    private double P;

    /**
     * Horizontal visibility during observation (0 = less than 100m, 1 = 100-200m, 2 = 200-300m, ..., 49 = 4900-5000m, 50 = 5-6km, 56 = 6-7km, 57 = 7- 8km, ...,
     *      * 79 = 29-30km, 80 = 30-35km, 81 = 35-40km, ..., 89 = more than 70km)
     * */
    private double VV;

    /**
     * Cloudy (coverage of the upper air in eighths), during the observation (9 = upper air invisible)
     * */
    private double N;

    /**
     * Relative humidity (in percent) at 1.50 m height during the observation
     *
     * */
    private double YOU;

    /**
     * Weather code (00-99), visually (WW) or automatically (WaWa) observed,
     * for the current weather or the weather in the past hour. See http://bibliotheek.knmi.nl/scholierenpdf/weercodes_Nederland*/
    private double WW;

    /**
     * Weather code indicator for the method of observation on a manned or
     * automatic station (1 = manned using code from visual observations,
     * 2.3 = manned and omitted (no important weather phenomenon, no data), 4 = automatic and recorded (using code from visual observations), 5.6 = automatically and omitted (no significant weather phenomenon, no data), 7 = automatically using code from automatic observations)
     * */
    private double IX;

    /**
     * Fog 0 = not occurred, 1 = occurred during the previous hour and / or during the observation
     * */
    private double M;

    /**
     * Rain 0 = not occurred, 1 = occurred during the previous hour and / or during the observation
     * */
    private double R;

    /**
     * 	Snow 0 = not occurred, 1 = occurred during the previous hour and / or during the observation
     * */
    private double S;

    /***
     * 	Storm 0 = not occurred, 1 = occurred during the previous hour and / or during the observation
     */
    private double O;

    /**
     * Ice formation 0 = not occurred, 1 = occurred during the previous hour and / or during the observation
     * */
    private double Y;


    public Generator() {
        generate();
    }

    @Scheduled(fixedDelay = 1000*3600)
    public void generate(){
        DD = randomniser(0,100, 12);
        FH = randomniser(0,100, 15);
        FF = randomniser(0,100, 12);
        FX = randomniser(0,100, 12);
        T = randomniser(0,100, 12);
        T10N = randomniser(0,100, 12);
        TD = randomniser(0,100, 12);
        SQ = randomniser(0,100, 12);
        Q = randomniser(0,100, 12);
        DR = randomniser(0,100, 12);
        RH = randomniser(0,100, 12);
        P = randomniser(0,100, 12);
        VV = randomniser(0,100, 12);
        N = randomniser(0,100, 12);
        YOU = randomniser(0,100, 12);
        WW = randomniser(0,100, 12);
        IX = randomniser(0,100, 12);
        M = randomniser(0,100, 12);
        R = randomniser(0,100, 12);
        S = randomniser(0,100, 12);
        O = randomniser(0,100, 12);
        Y = randomniser(0,100, 12);
    }


    public double randomniser(double min, double max, double median){
        return  (Math.random()* ((max - min )+1)) + min + median;
    }

}
