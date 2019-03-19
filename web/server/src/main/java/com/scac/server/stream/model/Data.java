package com.scac.server.stream.model;

import com.scac.server.stream.utils.CsvReader;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Component
public class Data {
    private Map<String, String> map;

    public Data(){
        map = new HashMap<String, String>();
    }


}
