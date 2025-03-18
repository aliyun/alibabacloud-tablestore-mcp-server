package com.alicloud.openservices.tablestore.sample.service;

import ai.djl.Application;
import ai.djl.Device;
import ai.djl.huggingface.translator.TextEmbeddingTranslatorFactory;
import ai.djl.inference.Predictor;
import ai.djl.repository.Artifact;
import ai.djl.repository.zoo.Criteria;
import ai.djl.repository.zoo.ModelNotFoundException;
import ai.djl.repository.zoo.ModelZoo;
import ai.djl.repository.zoo.ZooModel;
import ai.djl.training.util.ProgressBar;
import com.alicloud.openservices.tablestore.sample.config.EnvironmentSettings;
import jakarta.annotation.PreDestroy;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.io.Closeable;
import java.io.IOException;
import java.util.Collection;
import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class EmbeddingService implements Closeable {

    private final String modelName;
    private final ZooModel<String, float[]> model;

    public EmbeddingService() throws Exception {
        this.modelName = EnvironmentSettings.getEmbeddingModelName();
        log.info("use embedding model:{}", modelName);
        Criteria<String, float[]> criteria = Criteria.builder()
                .setTypes(String.class, float[].class)
                .optModelUrls("djl://" + modelName)
                .optTranslatorFactory(new TextEmbeddingTranslatorFactory())
                .optProgress(new ProgressBar())
                .build();
        this.model = criteria.loadModel();
    }

    public float[] embed(String text) {
        try (Predictor<String, float[]> predictor = model.newPredictor()) {
            return predictor.predict(text);
        } catch (Exception e) {
            throw new RuntimeException(String.format("embed text error: %s", text), e);
        }
    }

    /**
     * 列出支持的模型
     */
    public List<String> listModels() throws ModelNotFoundException, IOException {
        Criteria<?, ?> criteria = Criteria.builder()
                .optApplication(Application.NLP.TEXT_EMBEDDING)
                .optDevice(Device.cpu())
                .optProgress(new ProgressBar())
                .build();
        Map<Application, List<Artifact>> models = ModelZoo.listModels(criteria);
        return models.values().stream().flatMap(Collection::stream).map(artifact -> {
            StringBuilder sb = new StringBuilder(100);
            var metadata = artifact.getMetadata();
            if (metadata != null) {
                sb.append(metadata.getGroupId())
                        .append('/')
                        .append(metadata.getArtifactId())
                        .append('/');
            }
            if (artifact.getVersion() != null) {
                sb.append(artifact.getVersion()).append('/');
            }
            sb.append(artifact.getName());
            return sb.toString();
        }).toList();
    }

    @Override
    @PreDestroy
    public void close() throws IOException {
        log.info("closing embedding model:{}", modelName);
        if (model != null) {
            model.close();
        }
    }
}
