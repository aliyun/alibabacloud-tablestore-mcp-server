package com.alicloud.openservices.tablestore.sample.config;

public class EnvironmentSettings {

    public static String getTablestoreAccessKeyId() {
        return envSafe("TABLESTORE_ACCESS_KEY_ID");
    }

    public static String getTablestoreAccessKeySecret() {
        return envSafe("TABLESTORE_ACCESS_KEY_SECRET");
    }

    public static String getTablestoreEndpoint() {
        return envSafe("TABLESTORE_ENDPOINT");
    }

    public static String getTablestoreInstanceName() {
        return envSafe("TABLESTORE_INSTANCE_NAME");
    }

    public static int getVectorDimension() {
        return envOrDefault("TABLESTORE_VECTOR_DIMENSION", 768);
    }

    public static String getKnowledgeTableName() {
        return envOrDefault("TABLESTORE_KNOWLEDGE_TABLE_NAME", "knowledge_table_3");
    }

    public static String getKnowledgeIndexName() {
        return envOrDefault("TABLESTORE_KNOWLEDGE_INDEX_NAME", "index");
    }

    public static String getFAQTableName() {
        return envOrDefault("TABLESTORE_FAQ_TABLE_NAME", "faq_table_3");
    }

    public static String getFAQIndexName() {
        return envOrDefault("TABLESTORE_FAQ_INDEX_NAME", "index");
    }


    public static String getTablePkName() {
        return envOrDefault("TABLESTORE_TABLE_PK_NAME", "id");
    }

    public static String getTextFieldName() {
        return envOrDefault("TABLESTORE_TEXT_FIELD", "_content");
    }

    public static String getVectorFieldName() {
        return envOrDefault("TABLESTORE_VECTOR_FIELD", "_embedding");
    }

    public static String getEmbeddingModelName() {
        return envOrDefault("EMBEDDING_MODEL_NAME", "ai.djl.huggingface.rust/BAAI/bge-base-en-v1.5/0.0.1/bge-base-en-v1.5");
    }

    public static String getFAQAnswerFieldName() {
        return envOrDefault("TABLESTORE_FAQ_ANSWER_FIELD", "_answer");
    }

    private static String envOrDefault(String envName, String defaultValue) {
        String env = System.getenv(envName);
        if (env == null || env.isBlank()) {
            return defaultValue;
        }
        return env;
    }

    private static int envOrDefault(String envName, int defaultValue) {
        String env = System.getenv(envName);
        if (env == null || env.isBlank()) {
            return defaultValue;
        }
        return Integer.parseInt(env);
    }

    private static String envSafe(String envName) {
        String env = System.getenv(envName);
        if (env == null || env.isBlank()) {
            throw new IllegalArgumentException(String.format("environment variable '%s' is not set", envName));
        }
        return env;
    }

}
