package com.scac.server.stream.controller;

import com.scac.server.stream.utils.CsvReader;
import com.scac.server.stream.utils.Generator;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.util.HashMap;

@RestController
@RequestMapping(path = "/data", produces = "application/json")
public class DataController{

    {
        String file = "D:\\professional\\university\\master rug\\scalable computing\\git\\2019_group_4_s3555631_" +
            "s3795748_s3878708\\web\\server\\src\\main\\resources\\data\\data.csv";
        Thread t = new Thread(new CsvReader(file, 1000));
        t.start();
    }

    /*
    @Scheduled(fixedDelay = 1000)
    @GetMapping("/random")
    public String generateData(){
        Generator generator = new Generator();
        //generator.generate();
        return generator.toString();
    }*/


    @Scheduled(fixedDelay = 1000)
    @GetMapping("/csv")
    public HashMap<CsvReader.Headers, String> pushData() throws IOException {
        System.out.println(CsvReader.data);
        return CsvReader.data;
    }


}
