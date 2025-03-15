# 1. Running Method # 2 directly
## log:
```
WARNING:absl:No training configuration found in the save file, so the model was *not* compiled. Compile it manually.
2025-03-12 09:40:07.195353: I tensorflow/core/framework/local_rendezvous.cc:405] Local rendezvous is aborting with status: INVALID_ARGUMENT: indices[0,0] = 9 is not in [0, 3)
	 [[{{node functional_1/embedding_1/GatherV2}}]]
Traceback (most recent call last):
  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Lunar Byte/Synthetic_Data_Generator/synthetic_generator.py", line 118, in <module>
    main(args.config, args.out)
  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Lunar Byte/Synthetic_Data_Generator/synthetic_generator.py", line 101, in main
    synthetic_data = generate_gan_samples(generator, config, NOISE_DIM, labels_list, FS)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Lunar Byte/Synthetic_Data_Generator/synthetic_generator.py", line 54, in generate_gan_samples
    generated_sample = generator.predict([noise, label_indices], verbose=0)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/utils/traceback_utils.py", line 122, in error_handler
    raise e.with_traceback(filtered_tb) from None
  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/tensorflow/python/eager/execute.py", line 53, in quick_execute
    tensors = pywrap_tfe.TFE_Py_Execute(ctx._handle, device_name, op_name,
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tensorflow.python.framework.errors_impl.InvalidArgumentError: Graph execution error:

Detected at node functional_1/embedding_1/GatherV2 defined at (most recent call last):
  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Lunar Byte/Synthetic_Data_Generator/synthetic_generator.py", line 118, in <module>

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Lunar Byte/Synthetic_Data_Generator/synthetic_generator.py", line 101, in main

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Lunar Byte/Synthetic_Data_Generator/synthetic_generator.py", line 54, in generate_gan_samples

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/utils/traceback_utils.py", line 117, in error_handler

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/backend/tensorflow/trainer.py", line 560, in predict

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/backend/tensorflow/trainer.py", line 259, in one_step_on_data_distributed

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/backend/tensorflow/trainer.py", line 249, in one_step_on_data

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/backend/tensorflow/trainer.py", line 104, in predict_step

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/utils/traceback_utils.py", line 117, in error_handler

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/layers/layer.py", line 909, in __call__

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/utils/traceback_utils.py", line 117, in error_handler

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/ops/operation.py", line 52, in __call__

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/utils/traceback_utils.py", line 156, in error_handler

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/models/functional.py", line 183, in call

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/ops/function.py", line 171, in _run_through_graph

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/models/functional.py", line 643, in call

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/utils/traceback_utils.py", line 117, in error_handler

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/layers/layer.py", line 909, in __call__

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/utils/traceback_utils.py", line 117, in error_handler

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/ops/operation.py", line 52, in __call__

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/utils/traceback_utils.py", line 156, in error_handler

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/layers/core/embedding.py", line 140, in call

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/ops/numpy.py", line 5442, in take

  File "/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Byte War/byteWarSubmission/byteWarSubmission/env/lib/python3.11/site-packages/keras/src/backend/tensorflow/numpy.py", line 2222, in take

indices[0,0] = 9 is not in [0, 3)
	 [[{{node functional_1/embedding_1/GatherV2}}]] [Op:__inference_one_step_on_data_distributed_399]
```

## output: 
no output generated (output dir is empty)

# 2. Running Method # 1 directly:
## log
```
Synthetic data generated and saved to synthetic_data.csv
Generated CSV file copied to: output/synthetic_data_GAN3_500Epoch_4.csv
Running classifier_test.py from: /home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Lunar Byte/Synthetic_Data_Generator/classifier_test.py
Error running classifier_test.py: Command '['python', '/home/hem/projects/TechWeek2025_Hackathon/Synthetic_Data_Generator/Final_Five/Lunar Byte/Synthetic_Data_Generator/classifier_test.py']' returned non-zero exit status 2.

```

## output: 
- generates ```output/synthetic_data_GAN3_500Epoch_4.csv``` which does not matches with expected output which should be ```output/walking/walking1.csv ... {other walking csv files}``` 
```output/walking/running1.csv ... {other running csv files}```
so on

# 3. Method 1 followed by Method 2

## log:
```
WARNING:absl:No training configuration found in the save file, so the model was *not* compiled. Compile it manually.
Synthetic data generated and saved to output/synthetic_data_from_generator.csv
```

## output:

- generates ```output/synthetic_data_from_generator.csv``` which does not matches with expected output which should be ```output/walking/walking1.csv ... {other walking csv files}``` 
```output/walking/running1.csv ... {other running csv files}```
so on
