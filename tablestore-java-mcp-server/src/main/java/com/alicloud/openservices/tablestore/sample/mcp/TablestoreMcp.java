package com.alicloud.openservices.tablestore.sample.mcp;

import com.alicloud.openservices.tablestore.sample.model.Entry;
import com.alicloud.openservices.tablestore.sample.model.QueryRequest;
import com.alicloud.openservices.tablestore.sample.service.TablestoreService;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.function.FunctionToolCallback;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TablestoreMcp {


    @Bean
    public ToolCallbackProvider myTools(TablestoreService tablestoreService) {

        FunctionToolCallback<Entry, Void> storeTool = FunctionToolCallback.builder("store", tablestoreService::store)
                .description("Store document into Tablestore(表格存储) for later retrieval.")
                .inputType(Entry.class)
                .build();

        FunctionToolCallback<QueryRequest, List<Entry>> searchTools = FunctionToolCallback.builder("search", tablestoreService::search)
                .description("Search for similar documents on natural language descriptions from Tablestore(表格存储)")
                .inputType(QueryRequest.class)
                .build();

        return ToolCallbackProvider.from(List.of(
                storeTool,
                searchTools
        ));
    }
}
