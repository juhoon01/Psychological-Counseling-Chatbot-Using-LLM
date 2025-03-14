import threading
from queue import Queue
from time import sleep, time
from typing import List, Dict, Any

from ai.llm.models import MockModel
from log import logger


class ModelScheduler():
    def __init__(self):
        self.models = {}
        self.lock = threading.Lock()
        self.request_queues = {}
        self.last_request_time = {}
        self.timeout = 3600  # 1 hour

        # Start a thread to periodically clean up idle models
        cleanup_thread = threading.Thread(target=self._cleanup_idle_models)
        cleanup_thread.daemon = True
        cleanup_thread.start()

    def add_model(self, model_name, model):
        with self.lock:
            self.models[model_name] = model
            self.request_queues[model_name] = Queue()
            self.last_request_time[model_name] = time()

    def generate(self, model_name: str, prompt: str, histories: List[Dict[str, Any]] = []):
        if model_name not in self.models:
            return ''

        self.last_request_time[model_name] = time()

        result = Queue()
        self.request_queues[model_name].put((prompt, histories[:4], result))
        response = result.get()
        return response

    def _process_requests(self, model_name):
        while True:
            prompt, histories, result = self.request_queues[model_name].get()
            # str_histories = ''
            # for history in histories:
            #     str_histories += f"{str_histories}\n"
            # response = self.models[model_name].generate_response(f"{str_histories}\n\n{prompt}")
            response = self.models[model_name].generate_response(prompt)
            result.put(response)

    def start_processing(self):
        for model_name in self.models.keys():
            thread = threading.Thread(
                target=self._process_requests, args=(model_name,))
            thread.daemon = True
            thread.start()

    def _cleanup_idle_models(self):
        while True:
            with self.lock:
                current_time = time()
                to_remove = []
                for model_name, last_time in self.last_request_time.items():
                    if current_time - last_time > self.timeout:
                        to_remove.append(model_name)

                for model_name in to_remove:
                    logger.info(f"Removing idle model: {model_name}")
                    del self.models[model_name]
                    del self.request_queues[model_name]
                    del self.last_request_time[model_name]

            sleep(60)  # Check every minute


# Usage example
if __name__ == "__main__":
    scheduler = ModelScheduler()

    # Add models
    model_a = MockModel(model_name="ModelA")
    model_b = MockModel(model_name="ModelB")
    scheduler.add_model("ModelA", model_a)
    scheduler.add_model("ModelB", model_b)

    # Start processing requests
    scheduler.start_processing()

    # Generate responses
    def async_generate(scheduler, model_name, prompt):
        response = scheduler.generate(model_name, prompt)
        logger.info(
            f"Response from {model_name}: {response if response else 'No response'}")

    # Create threads to simulate asynchronous requests
    threading.Thread(target=async_generate, args=(
        scheduler, "ModelA", "Model A-1")).start()
    threading.Thread(target=async_generate, args=(
        scheduler, "ModelA", "Model A-2")).start()
    threading.Thread(target=async_generate, args=(
        scheduler, "ModelB", "Model B-1")).start()
    threading.Thread(target=async_generate, args=(
        scheduler, "ModelB", "Model B-2")).start()

    # Keep the main thread alive to let background threads finish
    while threading.active_count() > 1:
        sleep(0.1)
