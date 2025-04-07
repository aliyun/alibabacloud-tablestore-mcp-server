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
@JsonClassDescription("The document stored in FAQ store for later retrieval.")
public class FAQContent
{
    @JsonProperty(required = true, value = "question")
    @JsonPropertyDescription("a natural language document content")
    private String question = "";

    @JsonProperty(required = true, value = "answer")
    @JsonPropertyDescription("a natural language document content")
    private String answer = "";
}
