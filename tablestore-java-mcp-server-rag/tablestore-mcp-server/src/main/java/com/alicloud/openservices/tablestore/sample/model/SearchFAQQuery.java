package com.alicloud.openservices.tablestore.sample.model;

import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@ToString
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonClassDescription("The query request to search similar documents from faq store")
public class SearchFAQQuery
{

    @JsonProperty(required = true, value = "query")
    @JsonPropertyDescription("describe what you're looking for, and the tool will return the most relevant documents")
    private String query;

    @JsonProperty(required = false, value = "size")
    @JsonPropertyDescription("the number of similar documents to be returned")
    private int size = 20;
}
