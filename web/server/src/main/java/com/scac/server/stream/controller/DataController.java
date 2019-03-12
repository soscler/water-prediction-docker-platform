package com.scac.server.stream.controller;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(path = "/data", produces = "application/json")
public class DataController {

    /*@Scheduled(fixedDelay = 1000)
    public void scheduleFixedDelayTask() {
        System.out.println(
    }*/

    @Scheduled(fixedDelay = 1000)
    @GetMapping
    public String pushData(){
        return "Fixed delay task - " + System.currentTimeMillis() / 1000;
    }
}
