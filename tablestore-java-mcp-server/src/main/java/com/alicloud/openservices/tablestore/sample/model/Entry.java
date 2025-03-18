package com.alicloud.openservices.tablestore.sample.model;

import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.HashMap;
import java.util.Map;

@Data
@ToString
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonClassDescription("The document stored in Tablestore(表格存储) for later retrieval.")
public class Entry {

    @JsonProperty(required = true, value = "content")
    @JsonPropertyDescription("a natural language document content")
    private String content = "";

    @JsonProperty(required = false, value = "meta_data")
    @JsonPropertyDescription("a Python dictionary with strings as keys, which can store some meta data related to this document")
    private Map<String, Object> metaData = new HashMap<>();

}
