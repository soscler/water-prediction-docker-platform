package com.scac.server;

import com.scac.server.stream.utils.CsvReader;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

import java.io.IOException;

@SpringBootApplication
@EnableScheduling
public class ServerApplication {

    public static void main(String[] args) throws IOException {
        SpringApplication.run(ServerApplication.class, args);
        CsvReader csvReader = new CsvReader("D:\\professional\\university\\master rug\\scalable computing\\git\\2019_group_4_s3555631_s3795748_s3878708\\web\\server\\src\\main\\resources\\data\\data.csv",1000);
        csvReader.read();
    }
}
